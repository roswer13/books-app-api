"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'role',]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'role': {'required': False},
        }

    def create(self, validated_data):
        """Create a return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return the user."""

        if 'role' in validated_data:
            raise serializers.ValidationError("Role can't be changed.")

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token obtain pair serializer to include user role."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
