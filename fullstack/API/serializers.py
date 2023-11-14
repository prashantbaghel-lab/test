from rest_framework import serializers
#from rest_framework import 
from .models import device,tempratureReading, humidityData

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = device
        fields = ['uid', 'name']

# class DeviceListSerializer(serializers.ListSerializer):
#     child = DeviceSerializer()

class temperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = tempratureReading
        fields = '__all__'


class humiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = humidityData
        fields = '__all__'