from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser  # Importing abstractuser

from users.models import User

# Create your models here.

NOTIFICATION_TYPE = (
    ("New Appointment", "New Appointment"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)


# Doctors profile model
# This is the Doctor model that extends the User model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='doctor')
    image = models.FileField(upload_to="doctor_images", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    specialization = models.CharField(max_length=150, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.CharField(max_length=100, null=True, blank=True)
    next_availability = models.DateField(default=date.today)

    def __str__(self):
        return f" Dr. {self.full_name}"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        ordering = ["-id"]


# Notification model for doctor
class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey(
        "base.Appointment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='doctor_notifications'  
    )
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, null=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for Dr. {self.doctor.full_name} - {self.type}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date"]
