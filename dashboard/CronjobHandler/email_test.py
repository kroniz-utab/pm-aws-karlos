from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from dashboard.models import *
from datetime import datetime

def html_email():
    htmly = get_template('bee_template.html')

    today = datetime.today().strftime('%d-%m-%Y %H:%M')
    subject = f'Laporan Kondisi AWS {today}'

    recipient_list = [
        'adehf12@gmail.com', 
    ]

    # get data from model
    last_data = [
        Temperature.objects.order_by('-id')[0],
        Humidity.objects.order_by('-id')[0],
        Pressure.objects.order_by('-id')[0],
        SolarRadiation.objects.order_by('-id')[0],
        WindSpeed.objects.order_by('-id')[0],
        WindDir.objects.order_by('-id')[0],
        Precipitaion.objects.order_by('-id')[0],
    ]

    context = {
        'date': today,
        'data': []
    }

    html_content = htmly.render(context)

    msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=settings.EMAIL_HOST_USER, to=recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()