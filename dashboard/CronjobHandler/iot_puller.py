import requests
from dashboard.models import *

def _get_data_json():
    url = '' # URL from Thingspeak

    r = requests.get(url)

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None

# def update_db():
#     json = _get_data_json()
#     if json is not None:
#         try:
#             new_data = AwsData()

def coba_update():
    try:
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
    except:
        pass