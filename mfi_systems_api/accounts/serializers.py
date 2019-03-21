from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.Serializer):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)