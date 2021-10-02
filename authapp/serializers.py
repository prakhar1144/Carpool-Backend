from rest_framework.serializers import ModelSerializer
from .models import User

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        return User.objects.create_user(validated_data['email'], validated_data['password'])