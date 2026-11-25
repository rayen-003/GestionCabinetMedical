from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("appointment_date", "doctor", "patient", "status", "duration_minutes")
    list_filter = ("status", "doctor")
    search_fields = ("patient__last_name", "patient__national_id", "doctor__last_name")
    date_hierarchy = "appointment_date"
    readonly_fields = ("created_at", "updated_at")