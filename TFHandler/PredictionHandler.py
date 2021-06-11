import tensorflow as tf
from TFHandler.DataPreparation import (
    PreparationPrediction, PreparationPredictive
)
import pandas as pd
import numpy as np
import datetime
from pickle import load


class TemperaturePrediction():
    def __init__(self, queryset=None, value=None, is_rainy=None, timeAws=None):
        self.queryset = queryset
        self.value = value
        self.is_rainy = is_rainy
        self.timeAws = timeAws

        self.lstm_path = 'TFHandler/model/prediction/temp_prediction_w72.h5'
        self.class_path = 'TFHandler/model/classification/temp_classification.h5'
        self.scaler_path = 'TFHandler/scaler/temp_features_18.pkl'

        self.frame_lstm = self.lstm_step()

        self.pred_con = self.pred_maintenance()

    def predict_lstm(self, model, data, num_predict=72, lookback=72):
        data = data.reshape((-1))

        for _ in range(num_predict):
            x = data[-lookback:]
            x = x.reshape((1, lookback, 1))
            out = model.predict(x)[0][0]
            data = np.append(data, out)
        data = data[lookback-17:]

        return data
    
    def lstm_step(self):
        model = tf.keras.models.load_model(self.lstm_path)
        dt = PreparationPrediction(self.value, self.queryset, lookback=72)

        lstm_result = self.predict_lstm(model, dt.data_ready, num_predict=72, lookback=72)

        awstime = pd.to_datetime(self.timeAws)
        delta = datetime.timedelta(minutes=10)

        hour_class_list = []
        for _ in range(len(lstm_result)):
            awstime = awstime + delta
            hour_class = awstime.dt.hour
            hour_class_list.append(hour_class)
        
        hour_class_list = np.array(hour_class_list)
        df = pd.DataFrame({'value':lstm_result, 'hour_class':hour_class_list})
        df['is_rainy'] = self.is_rainy
        return df
    
    def oneHotEncoder(self, data):
        return [data[i].argmax() for i in range(len(data))]

    def pred_maintenance(self):
        class_model = tf.keras.models.load_model(self.class_path)
        scaler = load(open(self.scaler_path, 'rb'))

        dt = PreparationPredictive(self.frame_lstm).result
        dt[dt.columns] = scaler.transform(dt[dt.columns])

        y_pred = class_model.predict(dt)
        y_pred = self.oneHotEncoder(y_pred)

        y_error = [e for e in y_pred if e == 0]
        y_good = [g for g in y_pred if g == 1]
        y_suspect = [s for s in y_pred if s == 2]

        result = (round(len(y_error) / len(y_pred), 2),
                  round(len(y_good) / len(y_pred), 2),
                  round(len(y_suspect) / len(y_pred), 2))
        return result
        
class HumidityPrediction():
    def __init__(self, queryset=None, value=None, is_rainy=None, timeAws=None):
        self.queryset = queryset
        self.value = value
        self.is_rainy = is_rainy
        self.timeAws = timeAws

        self.lstm_path = 'TFHandler/model/prediction/rh_prediction_w72.h5'
        self.class_path = 'TFHandler/model/classification/rh_classification.h5'
        self.scaler_path = 'TFHandler/scaler/rh_features_18.pkl'

        self.frame_lstm = self.lstm_step()

        self.pred_con = self.pred_maintenance()

    def predict_lstm(self, model, data, num_predict=72, lookback=72):
        data = data.reshape((-1))

        for _ in range(num_predict):
            x = data[-lookback:]
            x = x.reshape((1, lookback, 1))
            out = model.predict(x)[0][0]
            data = np.append(data, out)
        data = data[lookback-17:]

        return data
    
    def lstm_step(self):
        model = tf.keras.models.load_model(self.lstm_path)
        dt = PreparationPrediction(self.value, self.queryset, lookback=72)

        lstm_result = self.predict_lstm(model, dt.data_ready, num_predict=72, lookback=72)

        awstime = pd.to_datetime(self.timeAws)
        delta = datetime.timedelta(minutes=10)

        hour_class_list = []
        for _ in range(len(lstm_result)):
            awstime = awstime + delta
            hour_class = awstime.dt.hour
            hour_class_list.append(hour_class)
        
        hour_class_list = np.array(hour_class_list)
        df = pd.DataFrame({'value':lstm_result, 'hour_class':hour_class_list})
        df['is_rainy'] = self.is_rainy
        return df
    
    def oneHotEncoder(self, data):
        return [data[i].argmax() for i in range(len(data))]

    def pred_maintenance(self):
        class_model = tf.keras.models.load_model(self.class_path)
        scaler = load(open(self.scaler_path, 'rb'))

        dt = PreparationPredictive(self.frame_lstm).result
        dt[dt.columns] = scaler.transform(dt[dt.columns])

        y_pred = class_model.predict(dt)
        y_pred = self.oneHotEncoder(y_pred)

        y_error = [e for e in y_pred if e == 0]
        y_good = [g for g in y_pred if g == 1]
        y_suspect = [s for s in y_pred if s == 2]

        result = (round(len(y_error) / len(y_pred), 2),
                  round(len(y_good) / len(y_pred), 2),
                  round(len(y_suspect) / len(y_pred), 2))
        return result

class SolarRadiationPrediction():
    def __init__(self, queryset=None, value=None, is_rainy=None, timeAws=None):
        self.queryset = queryset
        self.value = value
        self.is_rainy = is_rainy
        self.timeAws = timeAws

        self.lstm_path = 'TFHandler/model/prediction/sr_prediction_w72.h5'
        self.class_path = 'TFHandler/model/classification/sr_classification.h5'
        self.scaler_path = 'TFHandler/scaler/sr_features_18.pkl'

        self.frame_lstm = self.lstm_step()

        self.pred_con = self.pred_maintenance()

    def predict_lstm(self, model, data, num_predict=72, lookback=72):
        data = data.reshape((-1))

        for _ in range(num_predict):
            x = data[-lookback:]
            x = x.reshape((1, lookback, 1))
            out = model.predict(x)[0][0]
            data = np.append(data, out)
        data = data[lookback-17:]

        return data
    
    def lstm_step(self):
        model = tf.keras.models.load_model(self.lstm_path)
        dt = PreparationPrediction(self.value, self.queryset, lookback=72)

        lstm_result = self.predict_lstm(model, dt.data_ready, num_predict=72, lookback=72)

        awstime = pd.to_datetime(self.timeAws)
        delta = datetime.timedelta(minutes=10)

        hour_class_list = []
        for _ in range(len(lstm_result)):
            awstime = awstime + delta
            hour_class = awstime.dt.hour
            hour_class_list.append(hour_class)
        
        hour_class_list = np.array(hour_class_list)
        df = pd.DataFrame({'value':lstm_result, 'hour_class':hour_class_list})
        df['is_rainy'] = self.is_rainy
        return df
    
    def oneHotEncoder(self, data):
        return [data[i].argmax() for i in range(len(data))]

    def pred_maintenance(self):
        class_model = tf.keras.models.load_model(self.class_path)
        scaler = load(open(self.scaler_path, 'rb'))

        dt = PreparationPredictive(self.frame_lstm).result
        dt[dt.columns] = scaler.transform(dt[dt.columns])

        y_pred = class_model.predict(dt)
        y_pred = self.oneHotEncoder(y_pred)

        y_error = [e for e in y_pred if e == 0]
        y_good = [g for g in y_pred if g == 1]
        y_suspect = [s for s in y_pred if s == 2]

        result = (round(len(y_error) / len(y_pred), 2),
                  round(len(y_good) / len(y_pred), 2),
                  round(len(y_suspect) / len(y_pred), 2))
        return result

class WindDirectionPrediction():
    def __init__(self, queryset=None, value=None, is_rainy=None, timeAws=None):
        self.queryset = queryset
        self.value = value
        self.is_rainy = is_rainy
        self.timeAws = timeAws

        self.lstm_path = 'TFHandler/model/prediction/wd_prediction_w72.h5'
        self.class_path = 'TFHandler/model/classification/wd_classification.h5'
        self.scaler_path = 'TFHandler/scaler/wd_features_18.pkl'

        self.frame_lstm = self.lstm_step()

        self.pred_con = self.pred_maintenance()

    def predict_lstm(self, model, data, num_predict=72, lookback=72):
        data = data.reshape((-1))

        for _ in range(num_predict):
            x = data[-lookback:]
            x = x.reshape((1, lookback, 1))
            out = model.predict(x)[0][0]
            data = np.append(data, out)
        data = data[lookback-17:]

        return data
    
    def lstm_step(self):
        model = tf.keras.models.load_model(self.lstm_path)
        dt = PreparationPrediction(self.value, self.queryset, lookback=72)

        lstm_result = self.predict_lstm(model, dt.data_ready, num_predict=72, lookback=72)

        awstime = pd.to_datetime(self.timeAws)
        delta = datetime.timedelta(minutes=10)

        hour_class_list = []
        for _ in range(len(lstm_result)):
            awstime = awstime + delta
            hour_class = awstime.dt.hour
            hour_class_list.append(hour_class)
        
        hour_class_list = np.array(hour_class_list)
        df = pd.DataFrame({'value':lstm_result, 'hour_class':hour_class_list})
        df['is_rainy'] = self.is_rainy
        return df
    
    def oneHotEncoder(self, data):
        return [data[i].argmax() for i in range(len(data))]

    def pred_maintenance(self):
        class_model = tf.keras.models.load_model(self.class_path)
        scaler = load(open(self.scaler_path, 'rb'))

        dt = PreparationPredictive(self.frame_lstm).result
        dt[dt.columns] = scaler.transform(dt[dt.columns])

        y_pred = class_model.predict(dt)
        y_pred = self.oneHotEncoder(y_pred)

        y_error = [e for e in y_pred if e == 0]
        y_good = [g for g in y_pred if g == 1]
        y_suspect = [s for s in y_pred if s == 2]

        result = (round(len(y_error) / len(y_pred), 2),
                  round(len(y_good) / len(y_pred), 2),
                  round(len(y_suspect) / len(y_pred), 2))
        return result

class WindSpeedPrediction():
    def __init__(self, queryset=None, value=None, is_rainy=None, timeAws=None):
        self.queryset = queryset
        self.value = value
        self.is_rainy = is_rainy
        self.timeAws = timeAws

        self.lstm_path = 'TFHandler/model/prediction/ws_prediction_w72.h5'
        self.class_path = 'TFHandler/model/classification/wd_classification.h5'
        self.scaler_path = 'TFHandler/scaler/wd_features_18.pkl'

        self.frame_lstm = self.lstm_step()

        self.pred_con = self.pred_maintenance()

    def predict_lstm(self, model, data, num_predict=72, lookback=72):
        data = data.reshape((-1))

        for _ in range(num_predict):
            x = data[-lookback:]
            x = x.reshape((1, lookback, 1))
            out = model.predict(x)[0][0]
            data = np.append(data, out)
        data = data[lookback-17:]

        return data
    
    def lstm_step(self):
        model = tf.keras.models.load_model(self.lstm_path)
        dt = PreparationPrediction(self.value, self.queryset, lookback=72)

        lstm_result = self.predict_lstm(model, dt.data_ready, num_predict=72, lookback=72)

        awstime = pd.to_datetime(self.timeAws)
        delta = datetime.timedelta(minutes=10)

        hour_class_list = []
        for _ in range(len(lstm_result)):
            awstime = awstime + delta
            hour_class = awstime.dt.hour
            hour_class_list.append(hour_class)
        
        hour_class_list = np.array(hour_class_list)
        df = pd.DataFrame({'value':lstm_result, 'hour_class':hour_class_list})
        df['is_rainy'] = self.is_rainy
        return df
    
    def oneHotEncoder(self, data):
        return [data[i].argmax() for i in range(len(data))]

    def pred_maintenance(self):
        class_model = tf.keras.models.load_model(self.class_path)
        scaler = load(open(self.scaler_path, 'rb'))

        dt = PreparationPredictive(self.frame_lstm).result
        dt[dt.columns] = scaler.transform(dt[dt.columns])

        y_pred = class_model.predict(dt)
        y_pred = self.oneHotEncoder(y_pred)

        y_error = [e for e in y_pred if e == 0]
        y_good = [g for g in y_pred if g == 1]
        y_suspect = [s for s in y_pred if s == 2]

        result = (round(len(y_error) / len(y_pred), 2),
                  round(len(y_good) / len(y_pred), 2),
                  round(len(y_suspect) / len(y_pred), 2))
        return result