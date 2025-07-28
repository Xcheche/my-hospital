from django.contrib import admin
from doctor import models

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialization', 'image', 'qualification', 'years_of_experience','next_availability']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']


admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Notification,NotificationAdmin)