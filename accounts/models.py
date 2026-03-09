from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    STUDENT = 'STUDENT', _('Student')
    PATRON  = 'PATRON',  _('Patron (Teacher/Staff)')
    TRA     = 'TRA',     _('TRA Officer')

class EducationLevel(models.TextChoices):
    PRIMARY    = 'PRIMARY',   _('Primary School')
    SECONDARY  = 'SECONDARY', _('Secondary School')
    UNIVERSITY = 'UNIVERSITY',_('University/College')

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.STUDENT)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    level = models.CharField(max_length=20, choices=EducationLevel.choices)
    school_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, blank=True)
    points = models.IntegerField(default=0)

class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    staff_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100) # e.g., "Tax Education" or "School Patron"
    is_approved = models.BooleanField(default=False) # Staff need TRA approval