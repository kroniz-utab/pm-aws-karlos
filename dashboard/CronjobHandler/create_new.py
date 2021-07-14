from datetime import timedelta
import pandas as pd
import tensorflow as tf
import numpy as np
from pickle import load
from django_pandas.io import read_frame

import warnings
warnings.filterwarnings('ignore')


def sequence_maker(dataframe, window=6, dropna=True, is_ch=False):
    df = dataframe.copy()
    target = df.columns[0]

    for i in range(1, window):
        df[f'{target}{i}'] = df[target].shift(i)

    if dropna:
        df = df.dropna()
    else:
        df = df.fillna(0)

    if is_ch:
        result = df[[f'{target}{i}' for i in range(window - 1, 0, -1)]]
        result.loc[:, target] = df.loc[:, target]
        result.loc[:, 'is_rainy'] = df.loc[:, 'is_rainy']
    else:
        result = df[[f'{target}{i}' for i in range(window - 1, 0, -1)]]
        result.loc[:, target] = df.loc[:, target]
        result.loc[:, 'hour_class'] = df.loc[:, 'hour_class']
        result.loc[:, 'is_rainy'] = df.loc[:, 'is_rainy']

    return result


def oneHotDecoder(data):
    return np.array([dt.argmax() for dt in data])


def binaryDecoder(data):
    return np.array([0 if dt < 0.5 else 1 for dt in data])


def translate_class(id, is_categorical=True):
    if is_categorical:
        if id == 0:
            res = 'Error'
        elif id == 1:
            res = 'Good'
        else:
            res = 'Suspect'
    else:
        res = 'Good' if id == 0 else 'Suspect'
    return res


def save_val_only(models, val_now, hour_class, is_rainy):
    models.value = val_now
    models.hour_class = hour_class
    models.is_rainy = is_rainy
    models.save()


def save_no_pred(models, val_now, hour_class, is_rainy, status):
    models.value = val_now
    models.hour_class = hour_class
    models.is_rainy = is_rainy
    models.status = status
    models.save()


def save_all(models, val_now, hour_class, is_rainy, status, pred):
    models.value = val_now
    models.hour_class = hour_class
    models.is_rainy = is_rainy
    models.status = status
    models.pred_condition = pred
    models.save()


def newdf(queryset, val_now, hour_class, is_rainy, is_ch=False):
    if is_ch:
        df = read_frame(queryset, fieldnames=['value', 'is_rainy'])

        new_loc = df.index[-1] + 1
        df.loc[new_loc, 'value'] = val_now
        df.loc[new_loc, 'is_rainy'] = is_rainy
    else:
        df = read_frame(queryset, fieldnames=['value', 'hour_class', 'is_rainy'])

        new_loc = df.index[-1] + 1
        df.loc[new_loc, 'value'] = val_now
        df.loc[new_loc, 'hour_class'] = hour_class
        df.loc[new_loc, 'is_rainy'] = is_rainy
        
    return df


def from_dataframe(dataframe, idx):
    timestamp = dataframe.loc[idx, 'timestamp']
    ch = dataframe.loc[idx, 'ch']
    ws = dataframe.loc[idx, 'ws']
    wd = dataframe.loc[idx, 'wd']
    temp = dataframe.loc[idx, 'temp']
    rh = dataframe.loc[idx, 'rh']
    pa = dataframe.loc[idx, 'pa']
    sr = dataframe.loc[idx, 'sr']
    
    return timestamp, temp, rh, pa, sr, ws, wd, ch


def class_pred(dataframe, scaler_dir, class_dir, class_window, is_categorical=True):
    df = dataframe.copy()
    seq = sequence_maker(df, class_window, True)

    scaler = load(open(scaler_dir, 'rb'))
    seq[seq.columns] = scaler.transform(seq[seq.columns])

    class_model = tf.keras.models.load_model(class_dir, custom_objects={'tf':tf})
    
    y_pred = class_model.predict(seq)

    if is_categorical:
        res = oneHotDecoder(y_pred)
    else:
        res = binaryDecoder(y_pred)
    
    return res

def predict_qc(lstm_dir, class_dir, scaler_dir, full_dataframe, time_last, window_class=18, window_lstm=144, is_categorical=True, is_rainy=1):
    df = full_dataframe.copy()

    _datain = []
    _input = df.tail(window_lstm).filter(['value']).values
    _datain.append(_input)
    _datain = np.asarray(_datain).astype('float32')

    lstm_model = tf.keras.models.load_model(lstm_dir)

    y_pred = lstm_model.predict(_datain)
    y_pred = y_pred[0]
    y_pred = np.append(_datain[0, -17:, 0], y_pred)

    awstime = pd.Series(time_last)
    awstime = pd.to_datetime(awstime)
    delta = timedelta(minutes=10)
    awstime = awstime + delta

    hour_list = []
    for i in range(len(y_pred)):
        if i < 18:
            hour_list.append(0)
        else:
            hour_list.append(awstime.dt.hour.values[0])
            awstime = awstime + delta
    
    new_df = pd.DataFrame({'value':y_pred, 'hour_class':hour_list, 'is_rainy':is_rainy})

    pred_class = class_pred(new_df, scaler_dir, class_dir, window_class, is_categorical)

    if is_categorical:
        y_good = [g for g in pred_class if g == 1]
        y_sus = [s for s in pred_class if s == 2]
    else:
        y_good = [g for g in pred_class if g == 0]
        y_sus = [s for s in pred_class if s == 1]
    
    good_prob = len(y_good) / len(pred_class)
    sus_prob = len(y_sus) / len(pred_class)

    point = good_prob + sus_prob * 0.6

    return point
