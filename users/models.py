from django.db import models
from django.contrib.auth.models import AbstractUser  # Importing abstractuser

# Create your models here.


class User(AbstractUser):
    USER_TYPES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True, default='patient')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    

  

    def save(self, *args, **kwargs):
        if not self.username:  # cleaner way to check if username is empty or None
            email_username, _ = self.email.split(
                "@"
            )  # split email into username and domain
            self.username = email_username
        super().save(*args, **kwargs)
