"""
API views for departments app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Organization, Department, Position
from .serializers import (
    OrganizationSerializer, DepartmentSerializer, DepartmentListSerializer,
    DepartmentTreeSerializer, PositionSerializer, PositionListSerializer
)
from apps.accounts.permissions import IsSuperAdminOrAdmin


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing organizations.
    Only admins can create/update/delete organizations.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'short_name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        """Admin-only for write operations."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        """Get all departments of an organization."""
        organization = self.get_object()
        departments = organization.departments.filter(is_active=True, parent=None)
        serializer = DepartmentTreeSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get organization statistics."""
        organization = self.get_object()
        stats = {
            'total_departments': organization.departments.filter(is_active=True).count(),
            'total_employees': organization.get_total_employees(),
            'total_positions': organization.positions.filter(is_active=True).count(),
        }
        return Response(stats)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing departments.
    Supports hierarchical queries and tree operations.
    """
    queryset = Department.objects.select_related('organization', 'parent', 'head')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'parent', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['tree_id', 'lft']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return DepartmentListSerializer
        elif self.action == 'tree':
            return DepartmentTreeSerializer
        return DepartmentSerializer

    def get_permissions(self):
        """Admin-only for write operations."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get hierarchical tree of all departments."""
        organization_id = request.query_params.get('organization')
        if organization_id:
            departments = Department.objects.filter(
                organization_id=organization_id,
                parent=None,
                is_active=True
            )
        else:
            departments = Department.objects.filter(parent=None, is_active=True)
        serializer = DepartmentTreeSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in this department and sub-departments."""
        department = self.get_object()
        from apps.accounts.serializers import UserListSerializer
        employees = department.get_all_employees()
        serializer = UserListSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ancestors(self, request, pk=None):
        """Get all ancestor departments."""
        department = self.get_object()
        ancestors = department.get_ancestors()
        serializer = DepartmentListSerializer(ancestors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def descendants(self, request, pk=None):
        """Get all descendant departments."""
        department = self.get_object()
        descendants = department.get_descendants()
        serializer = DepartmentListSerializer(descendants, many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing positions.
    Defines job roles and their hierarchies.
    """
    queryset = Position.objects.select_related('organization', 'department', 'reports_to')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'department', 'level', 'is_active']
    search_fields = ['title', 'code']
    ordering_fields = ['level', 'title', 'created_at']
    ordering = ['level', 'title']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PositionListSerializer
        return PositionSerializer

    def get_permissions(self):
        """Admin-only for write operations."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def subordinate_positions(self, request, pk=None):
        """Get all positions that report to this position."""
        position = self.get_object()
        subordinates = Position.objects.filter(reports_to=position, is_active=True)
        serializer = PositionListSerializer(subordinates, many=True)
        return Response(serializer.data)
