from rest_framework import serializers 
from .models import Ride
from authapp.models import User

class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['destination','departure_time']

    def create(self, validated_data):
        # print(self.context['request'].user)
        ride = Ride(
                admin=self.context['request'].user,
                destination=validated_data['destination'],
                departure_time=validated_data['departure_time']
            )
        ride.save()
        ride.members.add(self.context['request'].user)
        return ride

# https://stackoverflow.com/a/57802461/14264497
class UserSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.id

    class Meta:
        model = User
        fields = ['id']

class RideSerializer(serializers.ModelSerializer):
    admin = serializers.CharField(source='admin.name')
    members = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Ride
        fields = "__all__"

class UpdateRideSerializer(serializers.ModelSerializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    class Meta:
        model = Ride
        fields = ['current_user']

    def update(self, instance, validated_data):
        print(self.context)
        print(instance.members.filter(id=validated_data['current_user'].id).exists())
        if instance.members.filter(id=validated_data['current_user'].id).exists():
            instance.members.remove(validated_data['current_user'])
        else:
            instance.members.add(validated_data['current_user'])
        return instance