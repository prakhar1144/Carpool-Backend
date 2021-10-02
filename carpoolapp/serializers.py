from django.db.models import fields
from rest_framework import serializers 
from .models import Ride

class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['destination','departure_time']

    def create(self, validated_data):
        print(self.context['request'].user)
        ride = Ride(
                admin=self.context['request'].user,
                destination=validated_data['destination'],
                departure_time=validated_data['departure_time']
            )
        ride.save()
        return ride

class RideSerializer(serializers.ModelSerializer):
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
        print(instance)
        instance.members.add(validated_data['current_user'])
        return instance