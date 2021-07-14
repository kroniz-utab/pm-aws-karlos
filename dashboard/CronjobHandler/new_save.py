from django_pandas.io import read_frame
import pandas as pd

from dashboard.models import *
from .create_new import *
from .email_report import html_email

def no_all(awstime, temp_now, rh_now, pa_now, sr_now, ws_now, wd_now, ch_now, is_rainy):
    aws_time = pd.Series(awstime)
    aws_time = pd.to_datetime(aws_time)
    hour_class = aws_time.dt.hour.values[0]
    minute_val = aws_time.dt.minute.values[0]

    # ============ Temperature =================
    temp = Temperature()
    save_val_only(temp, temp_now, hour_class, is_rainy)

    # ============ Humidity =================
    rh = Humidity()
    save_val_only(rh, rh_now, hour_class, is_rainy)

    # ============ Pressure =================
    pa = Pressure()
    save_val_only(pa, pa_now, hour_class, is_rainy)

    # ============ Wind Speed =================
    ws = WindSpeed()
    save_val_only(ws, ws_now, hour_class, is_rainy)

    # ============ Wind Dir =================
    wd = WindDir()
    save_val_only(wd, wd_now, hour_class, is_rainy)

    # ============ Solar Rad =================
    sr = SolarRadiation()
    save_val_only(sr, sr_now, hour_class, is_rainy)

    # ============ Precipitaion =================
    ch = Precipitaion()
    if hour_class == 0 and minute_val == 0:
        save_val_only(ch, ch_now, hour_class, is_rainy)
    else:
        pass
    
    # Wrap up
    data = AwsData()
    data.awsTime = awstime
    data.temp = Temperature.objects.latest('id')
    data.rh = Humidity.objects.latest('id')
    data.press = Pressure.objects.latest('id')
    data.solrad = SolarRadiation.objects.latest('id')
    data.winddir = WindDir.objects.latest('id')
    data.windspeed = WindSpeed.objects.latest('id')
    data.ch = Precipitaion.objects.latest('id')
    data.save()


def just_class(awstime, temp_now, rh_now, pa_now, sr_now, ws_now, wd_now, ch_now, is_rainy):
    aws_time = pd.Series(awstime)
    aws_time = pd.to_datetime(aws_time)
    hour_class = aws_time.dt.hour.values[0]
    minute_val = aws_time.dt.minute.values[0]

    # ============ Temperature =================
    # temp file dir
    temp_scaler = 'scaler/temp_features_18.pkl'
    temp_class = 'model/classification/temp_classification.h5'

    # process
    tqs = Temperature.objects.all()
    tdf = newdf(tqs, temp_now, hour_class, is_rainy, False) # full df
    tcdf = tdf.tail(18) # get df just for class pred
    temp_qc = class_pred(tcdf, temp_scaler, temp_class, 18, True)
    temp_translate = translate_class(temp_qc)

    temp = Temperature()
    save_no_pred(temp, temp_now, hour_class, is_rainy, temp_translate)

    # ============ Humidity =================
    # rh file dir
    rh_scaler = 'scaler/rh_features_18.pkl'
    rh_class = 'model/classification/rh_classification.h5'

    # process
    rqs = Humidity.objects.all()
    rdf = newdf(rqs, rh_now, hour_class, is_rainy, False)
    rcdf = rdf.tail(18)
    rh_qc = class_pred(rcdf, rh_scaler, rh_class, 18, True)
    rh_translate = translate_class(rh_qc)

    rh = Humidity()
    save_no_pred(rh, rh_now, hour_class, is_rainy, rh_translate)

    # ============ Pressure =================
    # pa file dir
    pa_scaler = 'scaler/pa_features_18.pkl'
    pa_class = 'model/classification/pa_classification.h5'

    # process
    pqs = Pressure.objects.all()
    pdf = newdf(pqs, pa_now, hour_class, is_rainy, False)
    pcdf = pdf.tail(18)
    pa_qc = class_pred(pcdf, pa_scaler, pa_class, 18, True)
    pa_translate = translate_class(pa_qc)

    pa = Pressure()
    save_no_pred(pa, pa_now, hour_class, is_rainy, pa_translate)

    # ============ Wind Speed =================
    # ws file dir
    ws_scaler = 'scaler/ws_features_18.pkl'
    ws_class = 'model/classification/ws_classification.h5'

    # process
    wsqs = WindSpeed.objects.all()
    wsdf = newdf(wsqs, ws_now, hour_class, is_rainy, False)
    wscdf = wsdf.tail(18)
    ws_qc = class_pred(wscdf, ws_scaler, ws_class, 18, True)
    ws_translate = translate_class(ws_qc)

    ws = WindSpeed()
    save_no_pred(ws, ws_now, hour_class, is_rainy, ws_translate)

    # ============ Wind Dir =================
    # ws file dir
    wd_scaler = 'scaler/wd_features_18.pkl'
    wd_class = 'model/classification/wd_classification.h5'

    # process
    wdqs = WindDir.objects.all()
    wddf = newdf(wdqs, wd_now, hour_class, is_rainy, False)
    wdcdf = wddf.tail(18)
    wd_qc = class_pred(wdcdf, wd_scaler, wd_class, 18, False)
    wd_translate = translate_class(wd_qc, is_categorical=False)

    wd = WindDir()
    save_no_pred(wd, wd_now, hour_class, is_rainy, wd_translate)

    # ============ Solar Rad =================
    # sr file dir
    sr_scaler = 'scaler/sr_features_18.pkl'
    sr_class = 'model/classification/sr_classification.h5'

    # process
    sds = SolarRadiation.objects.all()
    sdf = newdf(sds, sr_now, hour_class, is_rainy, False)
    scdf = sdf.tail(18)
    sr_qc = class_pred(scdf, sr_scaler, sr_class, 18, True)
    sr_translate = translate_class(sr_qc)

    sr = SolarRadiation()
    save_no_pred(sr, sr_now, hour_class, is_rainy, sr_translate)

    # ============ Precipitaion =================
    # ch file dir
    ch_scaler = 'scaler/sr_features_18.pkl'
    ch_class = 'model/classification/sr_classification.h5'

    ch = Precipitaion()
    if hour_class == 0 and minute_val == 0:
        if Precipitaion.objects.count() < 3:
            save_val_only(ch, ch_now, hour_class, is_rainy)
        else:
            cds = Precipitaion.objects.all()
            cdf = newdf(cds, ch_now, hour_class, is_rainy, True, is_ch=True)
            ccdf = cdf.tail(3)
            ch_qc = class_pred(ccdf, ch_scaler, ch_class, 3, False, is_ch=True)
            ch_translate = translate_class(ch_qc, is_categorical=False)

            save_no_pred(ch, ch_now, hour_class, is_rainy, ch_translate)
    else:
        pass

    # Wrap up
    data = AwsData()
    data.awsTime = awstime
    data.temp = Temperature.objects.latest('id')
    data.rh = Humidity.objects.latest('id')
    data.press = Pressure.objects.latest('id')
    data.solrad = SolarRadiation.objects.latest('id')
    data.winddir = WindDir.objects.latest('id')
    data.windspeed = WindSpeed.objects.latest('id')
    data.ch = Precipitaion.objects.latest('id')
    data.save()


def full_system(awstime, temp_now, rh_now, pa_now, sr_now, ws_now, wd_now, ch_now, is_rainy):
    aws_time = pd.Series(awstime)
    aws_time = pd.to_datetime(aws_time)
    hour_class = aws_time.dt.hour.values[0]
    minute_val = aws_time.dt.minute.values[0]

    # ============ Temperature =================
    # temp file dir
    temp_scaler = 'scaler/temp_features_18.pkl'
    temp_class = 'model/classification/temp_classification.h5'
    temp_lstm = 'model/prediction/ta_pred_model.h5'

    # process
    tqs = Temperature.objects.all()
    tdf = newdf(tqs, temp_now, hour_class, is_rainy, False)  # full df
    tcdf = tdf.tail(18)  # get df just for class pred
    temp_qc = class_pred(tcdf, temp_scaler, temp_class, 18, True)
    temp_translate = translate_class(temp_qc)
    temp_point = predict_qc(temp_lstm, temp_class, temp_scaler, tdf, awstime, 18, 144, True, is_rainy)
    temp_point = temp_point * 100

    temp = Temperature()
    save_all(temp, temp_now, hour_class, is_rainy, temp_translate, temp_point)

    # ============ Humidity =================
    # rh file dir
    rh_scaler = 'scaler/rh_features_18.pkl'
    rh_class = 'model/classification/rh_classification.h5'
    rh_lstm = 'model/prediction/rh_pred_model.h5'

    # process
    rqs = Humidity.objects.all()
    rdf = newdf(rqs, rh_now, hour_class, is_rainy, False)
    rcdf = rdf.tail(18)
    rh_qc = class_pred(rcdf, rh_scaler, rh_class, 18, True)
    rh_translate = translate_class(rh_qc)
    rh_point = predict_qc(rh_lstm, rh_class, rh_scaler, rdf, awstime, 18, 144, True, is_rainy)
    rh_point = rh_point * 100

    rh = Humidity()
    save_all(rh, rh_now, hour_class, is_rainy, rh_translate, rh_point)

    # ============ Pressure =================
    # pa file dir
    pa_scaler = 'scaler/pa_features_18.pkl'
    pa_class = 'model/classification/pa_classification.h5'
    pa_lstm = 'model/prediction/pa_pred_model.h5'

    # process
    pqs = Pressure.objects.all()
    pdf = newdf(pqs, pa_now, hour_class, is_rainy, False)
    pcdf = pdf.tail(18)
    pa_qc = class_pred(pcdf, pa_scaler, pa_class, 18, True)
    pa_translate = translate_class(pa_qc)
    pa_point = predict_qc(pa_lstm, pa_class, pa_scaler, pdf, awstime, 18, 144, True, is_rainy)
    pa_point = pa_point * 100

    pa = Pressure()
    save_all(pa, pa_now, hour_class, is_rainy, pa_translate, pa_point)

    # ============ Wind Speed =================
    # ws file dir
    ws_scaler = 'scaler/ws_features_18.pkl'
    ws_class = 'model/classification/ws_classification.h5'
    ws_lstm = 'model/prediction/ws_pred_model.h5'

    # process
    wsqs = WindSpeed.objects.all()
    wsdf = newdf(wsqs, ws_now, hour_class, is_rainy, False)
    wscdf = wsdf.tail(18)
    ws_qc = class_pred(wscdf, ws_scaler, ws_class, 18, True)
    ws_translate = translate_class(ws_qc)
    ws_point = predict_qc(ws_lstm, ws_class, ws_scaler, wsdf, awstime, 18, 144, True, is_rainy)
    ws_point = ws_point * 100

    ws = WindSpeed()
    save_all(ws, ws_now, hour_class, is_rainy, ws_translate, ws_point)

    # ============ Wind Dir =================
    # ws file dir
    wd_scaler = 'scaler/wd_features_18.pkl'
    wd_class = 'model/classification/wd_classification.h5'
    wd_lstm = 'model/prediction/wd_pred_model.h5'

    # process
    wdqs = WindDir.objects.all()
    wddf = newdf(wdqs, wd_now, hour_class, is_rainy, False)
    wdcdf = wddf.tail(18)
    wd_qc = class_pred(wdcdf, wd_scaler, wd_class, 18, False)
    wd_translate = translate_class(wd_qc, is_categorical=False)
    wd_point = predict_qc(wd_lstm, wd_class, wd_scaler, wddf, awstime, 18, 144, False, is_rainy)
    wd_point = wd_point * 100

    wd = WindDir()
    save_all(wd, wd_now, hour_class, is_rainy, wd_translate, wd_point)

    # ============ Solar Rad =================
    # sr file dir
    sr_scaler = 'scaler/sr_features_18.pkl'
    sr_class = 'model/classification/sr_classification.h5'
    sr_lstm = 'model/prediction/sr_pred_model.h5'

    # process
    sds = SolarRadiation.objects.all()
    sdf = newdf(sds, sr_now, hour_class, is_rainy, False)
    scdf = sdf.tail(18)
    sr_qc = class_pred(scdf, sr_scaler, sr_class, 18, True)
    sr_translate = translate_class(sr_qc)
    sr_point = predict_qc(sr_lstm, sr_class, sr_scaler, sdf, awstime, 18, 144, True, is_rainy)
    sr_point = sr_point * 100

    sr = SolarRadiation()
    save_all(sr, sr_now, hour_class, is_rainy, sr_translate, sr_point)

    # ============ Precipitaion =================
    # ch file dir
    ch_scaler = 'scaler/sr_features_18.pkl'
    ch_class = 'model/classification/sr_classification.h5'
    ch_lstm = 'model/prediction/ch_pred_model.h5'

    ch = Precipitaion()
    if hour_class == 0 and minute_val == 0:
        if Precipitaion.objects.count() < 3:
            save_val_only(ch, ch_now, hour_class, is_rainy)
        else:
            cds = Precipitaion.objects.all()
            cdf = newdf(cds, ch_now, hour_class, is_rainy, True, is_ch=True)
            ccdf = cdf.tail(3)
            ch_qc = class_pred(ccdf, ch_scaler, ch_class, 3, False, is_ch=True)
            ch_translate = translate_class(ch_qc, is_categorical=False)
            ch_point = predict_qc(ch_lstm, ch_class, ch_scaler, cdf, awstime, 3, 3, False, is_rainy, is_ch=True)
            ch_point = ch_point * 100

            save_all(ch, ch_now, hour_class, is_rainy, ch_translate, ch_point)
    else:
        pass

    # Wrap up
    data = AwsData()
    data.awsTime = awstime
    data.temp = Temperature.objects.latest('id')
    data.rh = Humidity.objects.latest('id')
    data.press = Pressure.objects.latest('id')
    data.solrad = SolarRadiation.objects.latest('id')
    data.winddir = WindDir.objects.latest('id')
    data.windspeed = WindSpeed.objects.latest('id')
    data.ch = Precipitaion.objects.latest('id')
    data.save()

    if hour_class == 0 and minute_val == 0:
        html_email(awstime)
