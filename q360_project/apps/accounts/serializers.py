"""
Serializers for accounts app API endpoints.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile, Role


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""

    class Meta:
        model = Role
        fields = ['id', 'name', 'display_name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""

    years_of_service = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            'date_of_birth', 'hire_date', 'education_level', 'specialization',
            'work_email', 'work_phone', 'address', 'language_preference',
            'email_notifications', 'sms_notifications', 'years_of_service'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with profile information."""

    profile = ProfileSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.get_full_name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'middle_name', 'last_name',
            'full_name', 'role', 'department', 'department_name', 'position',
            'phone_number', 'employee_id', 'profile_picture', 'bio',
            'supervisor', 'supervisor_name', 'is_active', 'date_joined',
            'last_login', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'middle_name', 'last_name', 'role',
            'department', 'position', 'phone_number', 'employee_id',
            'supervisor'
        ]

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Şifrələr uyğun gəlmir."}
            )
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Create associated profile
        Profile.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing users."""

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'middle_name', 'last_name',
            'role', 'department', 'position', 'phone_number',
            'profile_picture', 'bio', 'supervisor', 'is_active'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing user password."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Yeni şifrələr uyğun gəlmir."}
            )
        return attrs

    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Köhnə şifrə düzgün deyil.")
        return value


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for user lists."""

    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name', 'email',
            'role', 'role_display', 'department_name', 'position',
            'is_active', 'is_superuser'
        ]
