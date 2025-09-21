from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
#Import stripe for payment processing and pip install stripe
import stripe
from django.views.decorators.http import require_POST
import json
from datetime import date
# Create your views here.



# ==============Home View=====================
def home(request):
    """Render the home page with a list of published services."""
    services = base_models.Service.published.filter(status='PB').order_by('-publish')[:6]
    context = {'services': services}
    return render(request, "base/index.html", context)



# ===========Service Detail View=========
def service_detail(request, year, month, day, service_slug):
    """Display detailed information about a specific service."""
    target_date = date(int(year), int(month), int(day))
    service = get_object_or_404(
        base_models.Service.published,
        slug=service_slug,
        publish__date=target_date
    )
    context = {'service': service}
    return render(request, "base/service_detail.html", context)



# ============Book Appointment View===========
@login_required
def book_appointment(request, service_id, doctor_id):
    """Handle the booking of an appointment with a doctor for a specific service."""
    error = {}
    # Fetch the service, doctor, and patient objects
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    
    try:
        patient = patient_models.Patient.objects.get(user=request.user)
    except patient_models.Patient.DoesNotExist:
        patient = patient_models.Patient(user=request.user)
        patient.save()  # Save here!

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # Error validation
        if not full_name:
            error['full_name'] = "Full name is required."
        if not email:
            error['email'] = "Email is required."
        if not mobile:
            error['mobile'] = "Mobile number is required."
        if not gender:
            error['gender'] = "Gender is required."
        if not address:
            error['address'] = "Address is required."
        if not dob:
            error['dob'] = "Date of birth is required."
        if not issues:
            error['issues'] = "Issues are required."
        if not symptoms:
            error['symptoms'] = "Symptoms are required."
        if not doctor.next_availability:
            error['next_availability'] = "Doctor is not available for appointment."

        # Prevent duplicate active bookings
        if base_models.Appointment.objects.filter(
            patient=patient,
            service=service,
            doctor=doctor,
            status__in=['paid', 'Completed']  # Check for active appointments
        ).exists():
            messages.error(request, "You have already booked this appointment with this doctor and service.")
            context = {
                "service": service,
                "doctor": doctor,
                "patient": patient,
                "error": error,
            }
            return render(request, "base/book_appointment.html", context)

        # Update patient bio data
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.dob = dob
        patient.save()

        # Create appointment
        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_availability,
            issues=issues,
            symptoms=symptoms,
        )

        # Create billing
        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100  # 5% tax
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()

        messages.success(request, "Appointment booked successfully!")
        return redirect("checkout", billing.billing_id)

    # Render the booking form template with context
    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
        "error": error,
    }
    return render(request, "base/book_appointment.html", context)




# ============Checkout View===========
@login_required
def checkout(request, billing_id):  
    """Render the checkout page with billing details and payment options."""   


    billing = get_object_or_404(base_models.Billing, billing_id=billing_id)
    context = {
        "billing": billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    }
    return render(request, "base/checkout.html", context)




# ===========Stripe Payment Integration===========

@csrf_exempt
def stripe_payment(request, billing_id):
    """Create a Stripe checkout session for the given billing ID."""
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.patient.email,
        payment_method_types=['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'USD',
                    'product_data': {
                        'name': billing.patient.full_name
                    },
                    'unit_amount': int(billing.total * 100)
                },
                'quantity': 1
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse("stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"
        
    )
    return JsonResponse({"sessionId": checkout_session.id})



#====Verify payment===============
def stripe_payment_verify(request, billing_id):
    """Verify Stripe payment and update billing and appointment status."""
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid": #Payment was successful be sure to change appointment status to completed
        if billing.status == "Unpaid":
            billing.status = "Paid"
            billing.save()
            billing.appointment.status = "Completed"
            billing.appointment.save()

            doctor_models.Notification.objects.create(
                doctor=billing.appointment.doctor,
                appointment=billing.appointment,
                type="New Appointment"
            )

            patient_models.Notification.objects.create(
                patient=billing.appointment.patient,
                appointment=billing.appointment,
                type="Appointment Scheduled"
            )

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    
#=========Paypal=======    
#TODO: Paypal payment integration can be added here

    

# ============Payment Status View===========
@login_required
def payment_status(request, billing_id):
    """Display payment status to the user."""
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing": billing,
        "payment_status": payment_status,
    }
    return render(request, "base/payment_status.html", context)

