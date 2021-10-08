from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import User

class CreateAccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {'password': {'write_only': True},'email': {'write_only': True}}
    
    def create(self, validated_data):
        return User.objects.create_user(validated_data['email'], validated_data['password'])

class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'write_only': True}}

class LoginSerializer(Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(max_length=30, required=True, write_only=True)

class ForgotPasswordSerializer(Serializer):
    email = serializers.EmailField(write_only=True, required=False)
    new_password = serializers.CharField(min_length=5, max_length=30, write_only=True, required=False)
    user_id = serializers.IntegerField(write_only=True, required=False)
    secret_code = serializers.CharField(write_only=True, required=False)