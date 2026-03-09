from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, StaffProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile Information'

class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Profile Information'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # This ensures the correct profile shows up based on the user's role
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        if obj.role == 'STUDENT':
            return [StudentProfileInline(self.model, self.admin_site)]
        return [StaffProfileInline(self.model, self.admin_site)]

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'school_name', 'points')
    list_filter = ('level', 'school_name')
    search_fields = ('user__email', 'school_name')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'department', 'is_approved')
    list_filter = ('is_approved', 'department')
    actions = ['approve_staff']

    @admin.action(description='Approve selected staff members')
    def approve_staff(self, request, queryset):
        queryset.update(is_approved=True)