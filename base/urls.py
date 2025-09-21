from django.urls import path
from . import views


urlpatterns = [
    #====Service Booking System====
    path("", views.home, name="home"),
    # Service detail view with date and slug for SEO
    path("<int:year>/<int:month>/<int:day>/<slug:service_slug>/", views.service_detail, name="service_detail"),
    # Booking appointment with service and doctor IDs
    path("book/<int:service_id>/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    # Checkout process with billing ID
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
   
    #====Payment Integration====
    path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    # Stripe payment verification webhook
    path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
    # PayPal payment initiation



    
    #Final payment success page for both stripe and paypal or other payment gateways
    path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),

]
