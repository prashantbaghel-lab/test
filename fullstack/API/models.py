from django.db import models

# Create your models here.

class device(models.Model):
    uid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)


    def __str__(self):
        return self.name

class tempratureReading(models.Model):
    uid=models.ForeignKey(device, on_delete=models.CASCADE)
    temp=models.CharField(max_length=10)
    Date=models.DateTimeField(auto_now_add=True)


    

class humidityData(models.Model):
    uid=models.ForeignKey(device, on_delete=models.CASCADE)
    humidity=models.CharField(max_length=10)
    Date=models.DateTimeField(auto_now_add=True)


    
