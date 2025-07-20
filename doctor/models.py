from django.db import models
from django.contrib.auth.models import get_usermodel
# Create your models here.



class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.FileField(upload_to"doctor_images", null=True, blank=True)
    full_name = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=100,blank=True, null=True)
    country = models.CharField(max_length=100,null=True, balnk=True)
    bio = models.TextField(max_length=1000,null=True, blank=True)
    specialization = models.CharField(max_length=150,null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience =models.CharField(max_length=100,null=True, blank=TRue)
    next_availability = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user 