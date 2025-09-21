from django.contrib import admin
from doctor import models


# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialization', 'image', 'qualification', 'years_of_experience','next_availability']

# Admin classes for main models
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']

# Registering models with admin site
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Notification,NotificationAdmin)