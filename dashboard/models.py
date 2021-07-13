from os import name
from django.db import models

# Create your models here.
class Temperature(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='Temperature', null=True, blank=True)
    unit = models.CharField(max_length=50, default='C', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='Vaisala HMP155', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'temperature'
        managed = True

class Humidity(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='R. Humidity', null=True, blank=True)
    unit = models.CharField(max_length=50, default='%', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='Vaisala HMP155', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'humidity'
        managed = True

class Pressure(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='Air Pressure', null=True, blank=True)
    unit = models.CharField(max_length=50, default='mbar', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='RM Young 61302V', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pressure'
        managed = True

class WindSpeed(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='Wind Speed', null=True, blank=True)
    unit = models.CharField(max_length=50, default='m/s', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='Wind Monitor 05305', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'windspeed'
        managed = True

class WindDir(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='Wind Dir.', null=True, blank=True)
    unit = models.CharField(max_length=50, default='', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='Wind Monitor 05305', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'winddir'
        managed = True

class SolarRadiation(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='Solar Rad.', null=True, blank=True)
    unit = models.CharField(max_length=50, default='W/m^2', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='Kipp & Zonen SP Lite 2', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'solrad'
        managed = True

class Precipitaion(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=1)
    hour_class = models.IntegerField()
    is_rainy = models.IntegerField()
    status = models.CharField(max_length=50, default='Good')
    pred_condition = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    name = models.CharField(max_length=50, default='Precipitaion', null=True, blank=True)
    unit = models.CharField(max_length=50, default='mm', null=True, blank=True)
    sensor = models.CharField(max_length=50, default='TB3', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'precipitaion'
        managed = True

class AwsData(models.Model):
    awsTime = models.CharField(max_length=200)
    temp = models.ForeignKey(Temperature, on_delete=models.CASCADE)
    rh = models.ForeignKey(Humidity, on_delete=models.CASCADE)
    press = models.ForeignKey(Pressure, on_delete=models.CASCADE)
    solrad = models.ForeignKey(SolarRadiation, on_delete=models.CASCADE)
    winddir = models.ForeignKey(WindDir, on_delete=models.CASCADE)
    windspeed = models.ForeignKey(WindSpeed, on_delete=models.CASCADE)
    ch = models.ForeignKey(Precipitaion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aws_data'
        managed = True

class AwsDowntime(models.Model):
    awstime = models.CharField(max_length=200)
    parameter = models.CharField(max_length=50)
    message = models.CharField(max_length=250, default='')

    class Meta:
        db_table = 'aws_downtime'
        managed = True