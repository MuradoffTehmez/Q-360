"""
API views for accounts app.
"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Q, Count, Prefetch
from .models import User, Profile, Role
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserListSerializer, ProfileSerializer, RoleSerializer,
    PasswordChangeSerializer
)
from .permissions import IsSuperAdminOrAdmin, IsOwnerOrAdmin
from .security_utils import calculate_password_strength


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing roles.
    Only admins can view roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides CRUD operations with role-based access control.
    """
    queryset = User.objects.select_related('department', 'supervisor', 'profile')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'department', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['date_joined', 'last_name', 'first_name']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Filter queryset based on user role.
        - Superadmin/Admin sees all users
        - Manager sees their subordinates
        - Employee sees only themselves
        """
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superadmin() or user.is_admin():
            # Admin and Superadmin see all users
            return queryset
        elif user.is_manager():
            # Manager sees their subordinates
            return queryset.filter(supervisor=user)
        else:
            # Regular employee sees only themselves
            return queryset.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's information."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subordinates(self, request, pk=None):
        """Get all subordinates of a user."""
        user = self.get_object()
        subordinates = user.get_subordinates()
        serializer = UserListSerializer(subordinates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password."""
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"detail": "Şifrə uğurla dəyişdirildi."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a user account."""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(
            {"detail": "İstifadəçi aktivləşdirildi."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a user account."""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {"detail": "İstifadəçi deaktivləşdirildi."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def datatable(self, request):
        """
        DataTables API endpoint for dynamic table rendering.
        Supports server-side processing with pagination, search, and ordering.

        Query Parameters:
            - draw: DataTables draw counter
            - start: Starting record index
            - length: Number of records to return
            - search[value]: Global search value
            - order[0][column]: Column index for ordering
            - order[0][dir]: Order direction (asc/desc)
        """
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_idx = int(request.GET.get('order[0][column]', 0))
        order_dir = request.GET.get('order[0][dir]', 'asc')

        # Column mapping for ordering
        columns = ['id', 'username', 'first_name', 'last_name', 'email',
                   'department__name', 'position', 'role', 'is_active']

        # Get base queryset
        queryset = self.get_queryset()

        # Apply global search
        if search_value:
            queryset = queryset.filter(
                Q(username__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(employee_id__icontains=search_value) |
                Q(department__name__icontains=search_value) |
                Q(position__icontains=search_value)
            )

        # Get total count before pagination
        records_total = User.objects.count()
        records_filtered = queryset.count()

        # Apply ordering
        order_column = columns[order_column_idx] if order_column_idx < len(columns) else 'id'
        if order_dir == 'desc':
            order_column = f'-{order_column}'
        queryset = queryset.order_by(order_column)

        # Apply pagination
        queryset = queryset[start:start + length]

        # Serialize data
        serializer = UserListSerializer(queryset, many=True)

        # DataTables response format
        return Response({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': serializer.data
        })


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.
    Users can only update their own profile unless they're admin.
    """
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """Filter profiles based on user permissions."""
        user = self.request.user
        if user.is_admin():
            return super().get_queryset()
        return super().get_queryset().filter(user=user)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_password_strength(request):
    """
    Şifrə gücünü yoxlayan API endpoint.

    POST /api/accounts/check-password-strength/
    Body: {"password": "MyPassword123!"}

    Returns:
        {
            "score": 85,
            "strength": "Güclü",
            "feedback": ["Əla! Şifrəniz çox güclüdür."]
        }
    """
    password = request.data.get('password', '')

    if not password:
        return Response(
            {"error": "Şifrə daxil edilməlidir."},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = calculate_password_strength(password)
    return Response(result, status=status.HTTP_200_OK)
