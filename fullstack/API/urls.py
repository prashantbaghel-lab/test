#from django.contrib import admin
from django.urls import path
from .views import DeviceCreateView, DeviceDeleteView, DeviceListView, DeviceByUid, temperatureAdd, temperatureList, humidityAdd, humidityList, TemperatureHumidityGraphView
# from django.urls import path, include

urlpatterns = [
    path('api/devices/', DeviceCreateView.as_view(), name='device-create'),
    path('api/devices/<int:uid>/', DeviceDeleteView.as_view(), name='device-delete'),
    path('api/deviceslist/', DeviceListView.as_view(), name='device-list'),
    path('api/devicesretrive/<int:uid>', DeviceByUid.as_view(), name='device-byuid'),
    path('api/devices/tempratureadd', temperatureAdd.as_view(), name='device-create'),
    path('api/devices/<int:id>/readings/temp/', temperatureList.as_view(), name='temp-list'),
    path('api/devices/humidityAdd', humidityAdd.as_view(), name='humadity-create'),
    path('api/devices/<int:id>/readings/humadity/', humidityList.as_view(), name='temp-list'),
    path('api/temperature-humidity/graph/<int:device_id>/', TemperatureHumidityGraphView.as_view(), name='temperature-humidity-graph'),






    #path('admin/', admin.site.urls),
    #path("", include("API.urls"))
]