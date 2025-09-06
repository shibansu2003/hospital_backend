from django.contrib import admin
from .models import Patient, Doctor, PatientDoctor

#for development purpose only

# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "gender", "created_by", "created_at")
    search_fields = ("name", "created_by__username")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialization", "email", "created_by", "created_at")
    search_fields = ("name", "specialization", "email")

@admin.register(PatientDoctor)
class PatientDoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "assigned_by", "assigned_at")
    search_fields = ("patient__name", "doctor__name")
