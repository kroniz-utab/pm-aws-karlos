from django.db import models

# Create your models here.

class AwsDowntime(models.Model):
    awstime = models.CharField(max_length=200)
    parameter = models.CharField(max_length=50)
    message = models.CharField(max_length=250)
