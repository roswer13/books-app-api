"""
Views for user API.
"""
from rest_framework import generics, permissions

from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer, CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain pair view to include user role in the token."""
    serializer_class = CustomTokenObtainPairSerializer


class ManageUserView(
    generics.RetrieveUpdateAPIView,
    generics.DestroyAPIView,
):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authentication user."""
        return self.request.user
