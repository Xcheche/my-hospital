from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser  # Importing abstractuser

from users.models import User

# Create your models here.


# Choices for notification types
NOTIFICATION_TYPE = (
    ("Appointment Scheduled", "Appointment Scheduled"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)


# Patient profile model
#============== This is the Patient model that extends the User model================
class Patient(models.Model):
    """Patient model to extend the User model with additional fields specific to patients."""
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='patient')
    image = models.FileField(upload_to="patient_images", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.TextField(max_length=1000, null=True, blank=True)
    gender = models.CharField(max_length=150, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ["-id"]


#================== Notification model for patient=========================
class Notification(models.Model):
    """Notification model to handle notifications for patients."""
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True,  related_name="patient_notifications", blank=True
    )
    appointment = models.ForeignKey(
        "base.Appointment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="patient_appointments",
    )
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, null=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.patient.full_name} - {self.type}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date"]
