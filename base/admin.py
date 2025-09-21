from django.contrib import admin
from base import models
# Register your models here.
from import_export.admin import ImportExportModelAdmin

# Inline admin classes for related models
class AppointmentInline(admin.TabularInline):
    model = models.Appointment
    extra = 1


# Inline admin classes for related models
class MedicalRecordInline(admin.TabularInline):
    model = models.MedicalRecord
    extra = 1


# Inline admin classes for related models
class LabTestInline(admin.TabularInline):
    model = models.LabTest
    extra = 1


# Inline admin classes for related models    
class PrescriptionInline(admin.TabularInline):
    model = models.Prescription
    extra = 1



# Inline admin classes for related models
class BillingInline(admin.TabularInline):
    model = models.Billing
    extra = 1



# Admin classes for main models
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ['name', 'cost', 'status', 'publish']
    search_fields = ['name', 'description']
    filter_horizontal = ['available_doctors']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['cost', 'status']
    inlines = [AppointmentInline]




# Admin classes for main models
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status']
    search_fields = ['patient__username', 'doctor__user__username']
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline, BillingInline]



# Admin classes for main models
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis']



# Admin classes for main models
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'test_name']


# Admin classes for main models
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'medications']


# Admin classes for main models    

class BillingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'total', 'status', 'date']

    

# Registering models with admin site
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Appointment, AppointmentAdmin)
admin.site.register(models.MedicalRecord, MedicalRecordAdmin)
admin.site.register(models.LabTest, LabTestAdmin)
admin.site.register(models.Prescription, PrescriptionAdmin)
admin.site.register(models.Billing, BillingAdmin)

