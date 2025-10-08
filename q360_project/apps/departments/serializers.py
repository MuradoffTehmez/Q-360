"""
Serializers for departments app API endpoints.
"""
from rest_framework import serializers
from .models import Organization, Department, Position


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model."""

    total_employees = serializers.ReadOnlyField(source='get_total_employees')
    department_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'short_name', 'code', 'description',
            'address', 'phone', 'email', 'website',
            'is_active', 'established_date',
            'total_employees', 'department_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_department_count(self, obj):
        """Get number of departments in organization."""
        return obj.departments.filter(is_active=True).count()


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model with hierarchy information."""

    organization_name = serializers.CharField(source='organization.name', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    head_name = serializers.CharField(source='head.get_full_name', read_only=True)
    full_path = serializers.ReadOnlyField(source='get_full_path')
    employee_count = serializers.ReadOnlyField(source='get_employee_count')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'organization', 'organization_name', 'parent', 'parent_name',
            'name', 'code', 'description', 'phone', 'email', 'location',
            'head', 'head_name', 'is_active', 'full_path', 'employee_count',
            'level', 'lft', 'rght', 'tree_id', 'children',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'level', 'lft', 'rght', 'tree_id', 'created_at', 'updated_at']

    def get_children(self, obj):
        """Get immediate children departments."""
        children = obj.get_children().filter(is_active=True)
        return DepartmentListSerializer(children, many=True).data


class DepartmentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for department lists."""

    organization_name = serializers.CharField(source='organization.short_name', read_only=True)
    employee_count = serializers.ReadOnlyField(source='get_employee_count')

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'organization_name',
            'employee_count', 'is_active'
        ]


class DepartmentTreeSerializer(serializers.ModelSerializer):
    """Serializer for hierarchical department tree."""

    children = serializers.SerializerMethodField()
    employee_count = serializers.ReadOnlyField(source='get_employee_count')

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'employee_count', 'children']

    def get_children(self, obj):
        """Recursively get all children."""
        children = obj.get_children().filter(is_active=True)
        return DepartmentTreeSerializer(children, many=True).data


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for Position model."""

    organization_name = serializers.CharField(source='organization.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    reports_to_title = serializers.CharField(source='reports_to.title', read_only=True)

    class Meta:
        model = Position
        fields = [
            'id', 'organization', 'organization_name', 'department', 'department_name',
            'title', 'code', 'description', 'responsibilities',
            'level', 'reports_to', 'reports_to_title',
            'required_education', 'required_experience',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PositionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for position lists."""

    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Position
        fields = ['id', 'title', 'code', 'department_name', 'level', 'is_active']
