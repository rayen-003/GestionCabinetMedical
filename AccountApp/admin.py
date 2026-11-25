from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Doctor, Patient, Specialty, User


class DoctorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = ("username", "first_name", "last_name", "email", "license_number", "phone")


class PatientCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Patient
        fields = ("username", "first_name", "last_name", "email", "national_id", "phone", "birth_date")


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    add_form = DoctorCreationForm
    list_display = ("username", "first_name", "last_name", "license_number", "phone")
    search_fields = ("username", "first_name", "last_name", "license_number")
    list_filter = ("specialties",)
    filter_horizontal = ("specialties", "groups", "user_permissions")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations médecin", {"fields": ("license_number", "phone", "specialties")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email",
                       "license_number", "phone", "password1", "password2"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj:  # modification : identifiant métier non modifiable
            return (*readonly, "license_number")
        return readonly


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    add_form = PatientCreationForm
    list_display = ("username", "first_name", "last_name", "national_id", "phone", "birth_date")
    search_fields = ("username", "first_name", "last_name", "national_id")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations patient", {"fields": ("national_id", "phone", "birth_date")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email",
                       "national_id", "phone", "birth_date", "password1", "password2"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj:
            return (*readonly, "national_id")
        return readonly


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(User, UserAdmin)