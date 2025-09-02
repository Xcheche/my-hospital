# base/models.py
from django.utils import timezone
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from doctor import models as doctor_models
from patient import models as patient_models
from django.urls import reverse

# Create your models here.

# Service model for healthcare services
# This model represents a healthcare service that can be provided by doctors
# It includes fields for the service name, description, image, and cost.


# Custom manager to filter published services
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Service.Status.PUBLISHED)
    
# Service model    
class Service(models.Model):
    objects = models.Manager() 
    published = PublishedManager()  # Our custom manager.

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    image = models.FileField(upload_to="service_images", null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    description = models.TextField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)

    """
    This field is used to store the doctors who provide this service.
    It is a many-to-many relationship, meaning multiple doctors can provide the same service,
    and a doctor can provide multiple services.
    """
    available_doctors = models.ManyToManyField(
        doctor_models.Doctor, related_name="services", blank=True
    )
    """
    Decimal field is used for currency values, 
    max_digits is the total number of digits similar to max_length in CharField meaning it can  store even 10 bits of data or billions,
    and decimal_places is the number of digits after the decimal point

    """
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )


    def __str__(self):
        return  f'{self.name if self.name else "Service without name" } - {self.cost if self.cost else "No cost"}'


    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def get_absolute_url(self):
        return reverse(
            "service_detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "service_slug": self.slug,  # name "service" to match URLconf
            },
        )
  

# Appointment model for scheduling appointments between doctors and patients
class Appointment(models.Model):
    STATUS = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Pending", "Pending"),
        ("No Show", "No Show"),
        ("Cancelled", "Cancelled"),
    ]

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="appointments", null=True, blank=True
    )
    doctor = models.ForeignKey(
        doctor_models.Doctor, on_delete=models.CASCADE, related_name="appointments", null=True, blank=True
    )
    patient = models.ForeignKey(
        patient_models.Patient, on_delete=models.CASCADE, related_name="appointments", null=True, blank=True
    )
    appointment_time = models.DateTimeField(null=True, blank=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Scheduled")
    issues = models.TextField( null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    appointment_id = ShortUUIDField(
        length=6, max_length=10, alphabet="1234567890"
    )
    def __str__(self):
        return f'{self.patient.full_name} with {self.doctor.full_name} at {self.appointment_date.strftime("%Y-%m-%d %H:%M") if self.appointment_date else "No date"}'
    
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ["-appointment_date"]
        unique_together = ("appointment_id", "doctor", "appointment_date")
        constraints = [
            models.UniqueConstraint(
                fields=["appointment_id", "doctor", "appointment_date"],
                name="unique_appointment_per_doctor_per_date"
            )
        ]

    
# Medical Record model for appointments
class MedicalRecord(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name="medical_record",
        null=True, blank=True
    )
    treatment = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    extra_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Medical Record for {self.appointment.patient.full_name} - {self.appointment.appointment_id}"

    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ["-appointment__appointment_date"]


# Lab Test model for appointments
class LabTest(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name="lab_tests", null=True, blank=True
    )
    test_name = models.CharField(max_length=255, null=True, blank=True)
    test_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    lab_result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Lab Test: {self.test_name} for {self.appointment.patient.full_name}"

    class Meta:
        verbose_name = "Lab Test"
        verbose_name_plural = "Lab Tests"
        ordering = ["-test_date"]       

#Prescription
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name}"
    
    
#Billing
class Billing(models.Model):
    patient = models.ForeignKey(
        patient_models.Patient, on_delete=models.CASCADE,  null=True, blank=True
    )
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name="billings", null=True, blank=True
    )
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    """
    This field is used to store the payment status of the billing.
    It can be either "Paid" or "Unpaid".
    It has inline choices for better readability.
    """
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Unpaid", "Unpaid")], default="Unpaid")

    billing_id = ShortUUIDField(
        length=6, max_length=10, alphabet="1234567890"
    )
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Billing for {self.patient.full_name} - {self.billing_id} - Total: {self.total}"
