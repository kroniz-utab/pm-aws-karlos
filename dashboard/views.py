from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import pandas as pd

def savedata(model, value, hour_class, is_rainy, 
             status='Good', pred_condition=100.00):
    md = model()
    md.value = value
    md.hour_class = hour_class
    md.is_rainy = is_rainy
    md.status = status
    md.pred_condition = pred_condition
    md.save()

def from_csv(request):
    df = pd.read_csv('dashboard/data/dummy_data.csv')
    df = df.tail(100)
    df = df.reset_index(drop=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['jam'] = df['timestamp'].dt.hour
    musim = 1

    for i in range(len(df)):
        aws_time = df.loc[i, 'timestamp']
    
        # create object temp and save it
        temp = Temperature()
        temp.value = df.loc[i, 'temp']
        temp.hour_class = df.loc[i, 'jam']
        temp.is_rainy = musim
        temp.save()

        # create object humidity and save it
        rh = Humidity()
        rh.value = df.loc[i, 'rh']
        rh.hour_class = df.loc[i, 'jam']
        rh.is_rainy = musim
        rh.save()

        # create object pressure and save it
        pa = Pressure()
        pa.value = df.loc[i, 'pa']
        pa.hour_class = df.loc[i, 'jam']
        pa.is_rainy = musim
        pa.save()

        # create object WindSpeed and save it
        ws = WindSpeed()
        ws.value = df.loc[i, 'ws']
        ws.hour_class = df.loc[i, 'jam']
        ws.is_rainy = musim
        ws.save()

        # create object windDir and save it
        wd = WindDir()
        wd.value = df.loc[i, 'wd']
        wd.hour_class = df.loc[i, 'jam']
        wd.is_rainy = musim
        wd.save()

        # create object Solar Radiation and save it
        sr = SolarRadiation()
        sr.value = df.loc[i, 'sr']
        sr.hour_class = df.loc[i, 'jam']
        sr.is_rainy = musim
        sr.save()

        # create object Precipitation and save it
        ch = Precipitaion()
        ch.value = df.loc[i, 'ch']
        ch.hour_class = df.loc[i, 'jam']
        ch.is_rainy = musim
        ch.save()

        # create object AWS and save it
        data = AwsData()
        data.awsTime = aws_time
        data.temp = Temperature.objects.latest('id')
        data.rh = Humidity.objects.latest('id')
        data.press = Pressure.objects.latest('id')
        data.solrad = SolarRadiation.objects.latest('id')
        data.winddir = WindDir.objects.latest('id')
        data.windspeed = WindSpeed.objects.latest('id')
        data.ch = Precipitaion.objects.latest('id')
        data.save()

    return HttpResponse('Success!')

# Create your views here.
def entry(request):
    aws_time = '10-06-2021 04:30'
    
    # create object temp and save it
    temp = Temperature()
    temp.value = 28.6
    temp.hour_class = 4
    temp.is_rainy = 0
    temp.status = 'Suspect'
    temp.pred_condition = 80.77
    temp.save()

    # create object humidity and save it
    rh = Humidity()
    rh.value = 66.6
    rh.hour_class = 4
    rh.is_rainy = 0
    rh.status = 'Good'
    rh.pred_condition = 40.77
    rh.save()

    # create object pressure and save it
    pa = Pressure()
    pa.value = 1001.2
    pa.hour_class = 4
    pa.is_rainy = 0
    pa.status = 'Suspect'
    pa.pred_condition = 90.77
    pa.save()

    # create object WindSpeed and save it
    ws = WindSpeed()
    ws.value = 66.6
    ws.hour_class = 4
    ws.is_rainy = 0
    ws.status = 'Good'
    ws.pred_condition = 50.77
    ws.save()

    # create object windDir and save it
    wd = WindDir()
    wd.value = 359.3
    wd.hour_class = 4
    wd.is_rainy = 0
    wd.status = 'Good'
    wd.pred_condition = 65.77
    wd.save()

    # create object Solar Radiation and save it
    sr = SolarRadiation()
    sr.value = 752.4
    sr.hour_class = 4
    sr.is_rainy = 0
    sr.status = 'Suspect'
    sr.pred_condition = 70.77
    sr.save()

    # create object Precipitation and save it
    ch = Precipitaion()
    ch.value = 2.5
    ch.hour_class = 4
    ch.is_rainy = 0
    ch.status = 'Good'
    ch.pred_condition = 50.77
    ch.save()

    # create object AWS and save it
    data = AwsData()
    data.awsTime = aws_time
    data.temp_id = Temperature.objects.latest('id')
    data.rh_id = Humidity.objects.latest('id')
    data.press_id = Pressure.objects.latest('id')
    data.solrad_id = SolarRadiation.objects.latest('id')
    data.winddir_id = WindDir.objects.latest('id')
    data.windspeed_id = WindSpeed.objects.latest('id')
    data.ch_id = Precipitaion.objects.latest('id')
    data.save()

    return HttpResponse('Done')

@login_required(login_url='/login/')
def index(request):
    content = {
        'time':AwsData.objects.order_by('-id')[0],
        'data': [
            Temperature.objects.order_by('-id')[0],
            Humidity.objects.order_by('-id')[0],
            Pressure.objects.order_by('-id')[0],
            SolarRadiation.objects.order_by('-id')[0],
            WindSpeed.objects.order_by('-id')[0],
            WindDir.objects.order_by('-id')[0],
            Precipitaion.objects.order_by('-id')[0],
        ],
    }
    return render(request, 'dashboard.html', content)

@login_required(login_url='/login/')
def report(request):
    content = {
        'detail': [
            Temperature.objects.order_by('-id')[0],
            Humidity.objects.order_by('-id')[0],
            WindSpeed.objects.order_by('-id')[0],
            WindDir.objects.order_by('-id')[0],
            Pressure.objects.order_by('-id')[0],
            SolarRadiation.objects.order_by('-id')[0],
            Precipitaion.objects.order_by('-id')[0],
        ],
        'time':AwsData.objects.order_by('-id')[0],
    }
    return render(request, 'report.html', content)

def login_view(request):
    return render(request, 'login.html')

def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        messages.error(request, 'Login Gagal! Username atau Password Tidak Valid!')
        return redirect('login')

def logout_auth(request):
    logout(request)
    return redirect('/login/')