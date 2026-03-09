from rest_framework import serializers
from .models import CustomUser, StudentProfile, StaffProfile, UserRole, EducationLevel

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['level', 'school_name', 'registration_number', 'points']

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['staff_id', 'department', 'is_approved']

class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)
    staff_profile = StaffProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'student_profile', 'staff_profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    level = serializers.ChoiceField(choices=EducationLevel.choices, required=False)
    school_name = serializers.CharField(required=False, allow_blank=True)
    staff_id = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'role', 
                  'phone_number', 'level', 'school_name', 'staff_id', 'department')

   # accounts/serializers.py

    def create(self, validated_data):
        # ... (keep your extraction code the same) ...
        level = validated_data.pop('level', None)
        school_name = validated_data.pop('school_name', '')
        staff_id = validated_data.pop('staff_id', '')
        department = validated_data.pop('department', '')

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', UserRole.STUDENT),
            phone_number=validated_data.get('phone_number', '')
        )

        # FIX: Use get_or_create to prevent the "DoesNotExist" error
        if user.role == UserRole.STUDENT:
            profile, created = StudentProfile.objects.get_or_create(user=user)
            profile.level = level
            profile.school_name = school_name
            profile.save()
        else:
            profile, created = StaffProfile.objects.get_or_create(user=user)
            profile.staff_id = staff_id
            profile.department = department
            profile.save()

        return user