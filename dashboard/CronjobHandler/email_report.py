from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from dashboard.models import *
from datetime import datetime
from django_pandas.io import read_frame

def data_prep(queryset, last=144):
    df = read_frame(queryset, fieldnames=['name','status']).tail(last)
    df = df.reset_index(drop=True)

    prob_good = len(df[df['status'] == 'Good']) / len(df)
    prob_sus = len(df[df['status'] == 'Suspect']) / len(df)
    temp_point = (prob_good + prob_sus * 0.6) * 100
    temp_point = round(temp_point, 2)

    return temp_point, df.loc[0,'name']

def translate_point(point):
    if point >= 65:
        msg = 'Good'
    elif point < 65 and point > 50:
        msg = 'Suspectible'
    else:
        msg = 'Need Maintenance'
    
    return msg

def datainput(name, message, condition):
    data = {
        'name':name,
        'message':message,
        'condition':condition
    }
    return data

def html_email(now_time):
    # ================= Data Preparations =================
    # temp_data prep
    temp_qs = Temperature.objects.all()
    temp_point, temp_name = data_prep(temp_qs)
    temp_msg = translate_point(temp_point)
    temp_data = datainput(temp_name, temp_msg, temp_point)

    # rh_data prep
    rh_qs = Humidity.objects.all()
    rh_point, rh_name = data_prep(rh_qs)
    rh_msg = translate_point(rh_point)
    rh_data = datainput(rh_name, rh_msg, rh_point)

    # pa data prep
    pa_qs = Pressure.objects.all()
    pa_point, pa_name = data_prep(pa_qs)
    pa_msg = translate_point(pa_point)
    pa_data = datainput(pa_name, pa_msg, pa_point)

    # sr data prep
    sr_qs = SolarRadiation.objects.all()
    sr_point, sr_name = data_prep(sr_qs)
    sr_msg = translate_point(sr_point)
    sr_data = datainput(sr_name, sr_msg, sr_point)

    # wd data prep
    wd_qs = WindDir.objects.all()
    wd_point, wd_name = data_prep(wd_qs)
    wd_msg = translate_point(wd_point)
    wd_data = datainput(wd_name, wd_msg, wd_point)

    # ws data prep
    ws_qs = WindSpeed.objects.all()
    ws_point, ws_name = data_prep(ws_qs)
    ws_msg = translate_point(ws_point)
    ws_data = datainput(ws_name, ws_msg, ws_point)

    # ch data prep
    ch_qs = Precipitaion.objects.all()
    ch_point, ch_name = data_prep(ch_qs, 5)
    ch_msg = translate_point(ch_point)
    ch_data = datainput(ch_name, ch_msg, ch_point)


    htmly = get_template('bee_template.html')

    today = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')

    subject = f'Laporan Kondisi AWS {today}'

    recipient_list = [
        'adehf12@gmail.com',
        'adexxperient@gmail.com'
    ]

    # get data from model
    data = [
        temp_data,
        rh_data,
        pa_data,
        sr_data,
        ws_data,
        wd_data,
        ch_data
    ]

    context = {
        'date': today,
        'data': data
    }

    html_content = htmly.render(context)

    msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=settings.EMAIL_HOST_USER, to=recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
