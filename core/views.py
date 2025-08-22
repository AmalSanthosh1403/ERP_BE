from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from .serializers import RoleSerializer, UserSerializer
from rest_framework.response import Response
from .models import User, Role
from rest_framework.decorators import action
from .permissions import IsAdminPermission, CanManageUsers, CanViewEmployeesOnly, IsSelfOrAdmin

class LoginView(TokenObtainPairView):
    """
    Returns access and refresh tokens. Response also includes some user info.
    """
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        if resp.status_code == 200:
            # get user info (username/email is used in token obtain)
            username = request.data.get("username")
            user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
            if user:
                # add minimal user info
                resp.data.update({
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role.code if user.role else None,
                })
        return resp


class LogoutView(APIView):
    """
    Blacklist the refresh token (requires token_blacklist app).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "successfully logged out"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_superuser=True).select_related("role")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "list"]:
            return [CanManageUsers()]
        elif self.action == "list_employees":
            return [CanViewEmployeesOnly()]
        elif self.action == "me":
            return []  # just needs authentication
        else:
            return [IsSelfOrAdmin()]

    # Create User
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update User (PATCH or PUT)
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # always allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete User
    # destroy method is already defined in ModelViewSet, so it will not add response as per you code but status code will there -olny for destroy.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        """Admins can view all users if they have 'view_all_users' permission."""
        if request.user.is_authenticated and request.user.role and request.user.role.permissions.filter(code="view_all_users").exists():
            return super().list(request, *args, **kwargs)
        return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=["get"])
    def list_employees(self, request):
        """Managers can view employees only."""
        employees = User.objects.filter(role__is_employee=True)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def profile(self, request):
        """Return logged-in user's profile (any role)."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "list"]:
            return [IsAdminPermission()]
        return [IsAuthenticated()]

    # Create Role
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Role created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update Role (PATCH or PUT)
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Role updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Role
    # destroy method is already defined in ModelViewSet, so it will not add response as per our code but status code will there -olny for destroy.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Role deleted successfully"}, status=status.HTTP_200_OK)
