from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Temperature)
class TempAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(Humidity)
class HumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(Pressure)
class PressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(WindSpeed)
class WsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(WindDir)
class WdAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(SolarRadiation)
class SrAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(Precipitaion)
class ChAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'status', 'pred_condition')
    list_filter = ('created_at', 'status')


@admin.register(AwsData)
class AwsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'awsTime', 'temp', 'rh', 'press', 'solrad', 'winddir', 'windspeed', 'ch')
    list_filter = ('created_at', )
