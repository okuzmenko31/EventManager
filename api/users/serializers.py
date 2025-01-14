from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "is_active", "date_joined"]


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email must be unique!")],
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    def validate(self, attrs):
        if attrs["password1"] != attrs["password"]:
            raise serializers.ValidationError("Password mismatch.")
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("User with this email is already exists!")
        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user
