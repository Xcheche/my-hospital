from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models
from django.contrib import messages
from django.conf import settings
# Create your views here.

def home(request):
    services = base_models.Service.published.filter(status='PB').order_by('-publish')[:6]
    context = {'services': services}
    return render(request, "base/index.html", context)

from datetime import date

def service_detail(request, year, month, day, service_slug):
    target_date = date(int(year), int(month), int(day))
    service = get_object_or_404(
        base_models.Service.published,
        slug=service_slug,
        publish__date=target_date
    )
    context = {'service': service}
    return render(request, "base/service_detail.html", context)


#Make booking

@login_required
def book_appointment(request, service_id, doctor_id):
    error = {}
    # Fetch the service, doctor, and patient objects
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    try:
        patient = patient_models.Patient.objects.get(user=request.user)
    except patient_models.Patient.DoesNotExist:
        patient = patient_models.Patient(user=request.user)
        # Handle html form submission
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")


        #Error validation can be added here
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


        # Update patient bio data no need for a seperate orm or view
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.dob = dob
        patient.save()

        # Create appointment object using the create method
        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_availability,
            issues=issues,
            symptoms=symptoms,
        )

        # Create a billing objects using the save method
        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100  # 5% tax change according to policy or location/country
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


def checkout(request, billing_id):
    billing = get_object_or_404(base_models.Billing, billing_id=billing_id)
    context = {
        "billing": billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    }
    return render(request, "base/checkout.html", context)