from django.http import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *


@login_required(login_url='/login/')
def index(request):
    try:
        content = {
            'time': AwsData.objects.order_by('-id')[0],
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
    except:
        return render(request, '204.html')


@login_required(login_url='/login/')
def report(request):
    try:
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
            'time': AwsData.objects.order_by('-id')[0],
        }
        return render(request, 'report.html', content)
    except:
        return render(request, '204.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'login.html')


def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        messages.error(
            request, 'Login Gagal! Username atau Password Tidak Valid!')
        return redirect('login')


@login_required(login_url='/login/')
def logout_auth(request):
    logout(request)
    return redirect('/login/')

def page_404(request, exception):
    return render(request, '404.html')

def page_500(request):
    return render(request, '500.html')