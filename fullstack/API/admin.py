from django.contrib import admin
from .models import device, tempratureReading, humidityData

# Register your models here.

admin.site.register(device)
admin.site.register(tempratureReading)
admin.site.register(humidityData)
