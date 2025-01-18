from rest_framework import serializers
from .models import BeaconUser, BeaconDevice

class BeaconUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BeaconUser
        fields = ('id', 'email', 'username', 'password', 'role', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = BeaconUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'VIEWER')
        )
        return user

class BeaconDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeaconDevice
        fields = '__all__'