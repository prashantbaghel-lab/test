from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from rest_framework.views import APIView 
from rest_framework import generics
from .models import humidityData
from rest_framework.response import Response
from rest_framework import status
from .models import device, tempratureReading
from django.http import HttpResponse
import matplotlib

from .serializers import DeviceSerializer, temperatureSerializer, humiditySerializer
import matplotlib.pyplot as plt
import io
import base64
matplotlib.use('agg')


class DeviceCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeviceDeleteView(APIView):
    def delete(self, request, uid, *args, **kwargs):
        try:
            devices = device.objects.get(uid=uid)
        except devices.DoesNotExist:
            return Response({'detail': 'Device not found.'}, status=status.HTTP_404_NOT_FOUND)

        devices.delete()
        return Response({'detail': 'Device deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
class DeviceListView(APIView):
    def get(self, request):
        devices = device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceByUid(generics.RetrieveAPIView):
    queryset = device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'uid'

class temperatureAdd(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = temperatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class temperatureList(APIView):
    def get(self, request, id):
        startDate = request.query_params['startDate']
        endDate = request.query_params['endDate']
        devices = device.objects.filter(uid=id)
        temperatures = tempratureReading.objects.filter(Date__gte=startDate, Date__lte=endDate, uid=id)
        #temperatures = temperature.objects.filter(uid=id)
        if len(devices) != 0:
            devices = DeviceSerializer(devices, many=True)
            print(devices.data)
            if len(temperatures) != 0:
                temperatures = temperatureSerializer(temperatures, many=True)
                return Response(temperatures.data)
            else:
                return HttpResponse("No Temperature Recorded")    
        else:
            return HttpResponse("No Device Found with this Entered Id")
   


class humidityAdd(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = humiditySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class humidityList(APIView):
    def get(self, request, id):
        startDate = request.query_params['startDate']
        endDate = request.query_params['endDate']
        devices = device.objects.filter(uid=id)
        humiditydata = humidityData.objects.filter(Date__gte=startDate, Date__lte=endDate, uid=id)
        if len(devices) != 0:
            devices = DeviceSerializer(devices, many=True)
            print(devices.data)
            if len(humiditydata) != 0:
                humiditydata = humiditySerializer(humiditydata, many=True)
                return Response(humiditydata.data)
            else:
                return HttpResponse("No Humidity Recorded")    
        else:
            return HttpResponse("No Device Found with this Entered Id") 


class TemperatureHumidityGraphView(generics.RetrieveAPIView):
    temperature_serializer_class = temperatureSerializer
    humidity_serializer_class = humiditySerializer

    def retrieve(self, request, *args, **kwargs):
        device_id = kwargs.get('device_id')

        # Get temperature data for the given device ID
        temperature_queryset = tempratureReading.objects.filter(uid=device_id)
        temperature_serializer = self.temperature_serializer_class(temperature_queryset, many=True)

        # Get humidity data for the given device ID
        humidity_queryset = humidityData.objects.filter(uid=device_id)
        humidity_serializer = self.humidity_serializer_class(humidity_queryset, many=True)

        # Extract data for plotting
        temperature_data = temperature_serializer.data
        temperature_values = [entry['temp'] for entry in temperature_data]
        temperature_dates = [entry['Date'] for entry in temperature_data]

        humidity_data = humidity_serializer.data
        humidity_values = [entry['humidity'] for entry in humidity_data]
        humidity_dates = [entry['Date'] for entry in humidity_data]

        # Plotting
        plt.figure(figsize=(10,6))
        plt.plot(temperature_dates, temperature_values, label='Temperature', marker='o')
        plt.plot(humidity_dates, humidity_values, label='Humidity' ,  marker='o')
        plt.xlabel('Date')
        plt.ylabel('Temperature and Humidity')
        plt.legend()
        plt.title('Temperature and Humidity vs. Time')
        plt.xticks(rotation=45)
        plt.show() 

        # Save the plot to a BytesIO object
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        plt.close()

        # Encode the plot image as base64
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.read()).decode('utf-8')

        # Return the response with the HTML template
        return render(request, 'API/temperature_humidity_graph.html', {'plot_image': img_str})