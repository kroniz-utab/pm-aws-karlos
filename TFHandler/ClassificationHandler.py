import tensorflow as tf
from pickle import load
from .DataPreparation import PreparationClassification

class TemperatureClassifier():
    def __init__(self, queryset=None, 
                 value=None, 
                 hour_class=None, 
                 is_rainy=None):
        self.model_path = 'TFHandler/model/classification/temp_classification.h5'
        self.scaler_path = 'TFHandler/scaler/temp_features_18.pkl'
        self.queryset = queryset

        # new data from acquisition system
        self.new_value = value
        self.new_hour_class = hour_class
        self.new_is_rainy = is_rainy

        # output of predict class
        self.predict_class = None
    
    def fit(self):
        model = tf.keras.models.load_model(self.model_path)
        scaler = load(open(self.scaler_path, 'rb'))

        pc = PreparationClassification(queryset=self.queryset,
                                       value=self.new_value,
                                       hour_class=self.new_hour_class,
                                       is_rainy=self.new_is_rainy,
                                       window=18)
        pc.fit()
        dt = pc.data_ready
        dt[dt.columns] = scaler.transform(dt[dt.columns])
        feature = dt.values

        predict_class = model.predict(feature)

        # decode onehot
        predict_class = predict_class.argmax()
        self.predict_class = 'Error' if predict_class == 0 else 'Good' if predict_class == 1 else 'Suspect'

class HumidityClassifier():
    def __init__(self, queryset=None, 
                 value=None, 
                 hour_class=None, 
                 is_rainy=None):
        self.model_path = 'TFHandler/model/classification/rh_classification.h5'
        self.scaler_path = 'TFHandler/scaler/rh_features_18.pkl'
        self.queryset = queryset

        # new data from acquisition system
        self.new_value = value
        self.new_hour_class = hour_class
        self.new_is_rainy = is_rainy

        # output of predict class
        self.predict_class = None
    
    def fit(self):
        model = tf.keras.models.load_model(self.model_path)
        scaler = load(open(self.scaler_path, 'rb'))

        pc = PreparationClassification(queryset=self.queryset,
                                       value=self.new_value,
                                       hour_class=self.new_hour_class,
                                       is_rainy=self.new_is_rainy,
                                       window=18)
        pc.fit()
        dt = pc.data_ready
        dt[dt.columns] = scaler.transform(dt[dt.columns])
        feature = dt.values

        predict_class = model.predict(feature)

        # decode onehot
        predict_class = predict_class.argmax()
        self.predict_class = 'Error' if predict_class == 0 else 'Good' if predict_class == 1 else 'Suspect'

class SolarRadiationClassifier():
    def __init__(self, queryset=None, 
                 value=None, 
                 hour_class=None, 
                 is_rainy=None):
        self.model_path = 'TFHandler/model/classification/sr_classification.h5'
        self.scaler_path = 'TFHandler/scaler/sr_features_18.pkl'
        self.queryset = queryset

        # new data from acquisition system
        self.new_value = value
        self.new_hour_class = hour_class
        self.new_is_rainy = is_rainy

        # output of predict class
        self.predict_class = None
    
    def fit(self):
        model = tf.keras.models.load_model(self.model_path)
        scaler = load(open(self.scaler_path, 'rb'))

        pc = PreparationClassification(queryset=self.queryset,
                                       value=self.new_value,
                                       hour_class=self.new_hour_class,
                                       is_rainy=self.new_is_rainy,
                                       window=18)
        pc.fit()
        dt = pc.data_ready
        dt[dt.columns] = scaler.transform(dt[dt.columns])
        feature = dt.values

        predict_class = model.predict(feature)

        # decode onehot
        predict_class = predict_class.argmax()
        self.predict_class = 'Error' if predict_class == 0 else 'Good' if predict_class == 1 else 'Suspect'

class WindDirectionClassifier():
    def __init__(self, queryset=None, 
                 value=None, 
                 hour_class=None, 
                 is_rainy=None):
        self.model_path = 'TFHandler/model/classification/wd_classification.h5'
        self.scaler_path = 'TFHandler/scaler/wd_features_18.pkl'
        self.queryset = queryset

        # new data from acquisition system
        self.new_value = value
        self.new_hour_class = hour_class
        self.new_is_rainy = is_rainy

        # output of predict class
        self.predict_class = None
    
    def fit(self):
        model = tf.keras.models.load_model(self.model_path)
        scaler = load(open(self.scaler_path, 'rb'))

        pc = PreparationClassification(queryset=self.queryset,
                                       value=self.new_value,
                                       hour_class=self.new_hour_class,
                                       is_rainy=self.new_is_rainy,
                                       window=18)
        pc.fit()
        dt = pc.data_ready
        dt[dt.columns] = scaler.transform(dt[dt.columns])
        feature = dt.values

        predict_class = model.predict(feature)

        # decode onehot
        # predict_class = predict_class.argmax()
        self.predict_class = 'Good' if predict_class >= 0.5 else 'Suspect'

class WindSpeedClassification():
    def __init__(self, queryset=None, 
                 value=None, 
                 hour_class=None, 
                 is_rainy=None):
        self.model_path = 'TFHandler/model/classification/ws_classification.h5'
        self.scaler_path = 'TFHandler/scaler/ws_features_18.pkl'
        self.queryset = queryset

        # new data from acquisition system
        self.new_value = value
        self.new_hour_class = hour_class
        self.new_is_rainy = is_rainy

        # output of predict class
        self.predict_class = None
    
    def fit(self):
        model = tf.keras.models.load_model(self.model_path)
        scaler = load(open(self.scaler_path, 'rb'))

        pc = PreparationClassification(queryset=self.queryset,
                                       value=self.new_value,
                                       hour_class=self.new_hour_class,
                                       is_rainy=self.new_is_rainy,
                                       window=18)
        pc.fit()
        dt = pc.data_ready
        dt[dt.columns] = scaler.transform(dt[dt.columns])
        feature = dt.values

        predict_class = model.predict(feature)

        # decode onehot
        predict_class = predict_class.argmax()
        self.predict_class = 'Error' if predict_class == 0 else 'Good' if predict_class == 1 else 'Suspect'

class WindSpeedClassification():
    def __init__(self, queryset=None, 
                 value=None, 
                 hour_class=None, 
                 is_rainy=None):
        self.model_path = 'TFHandler/model/classification/ws_classification.h5'
        self.scaler_path = 'TFHandler/scaler/ws_features_18.pkl'
        self.queryset = queryset

        # new data from acquisition system
        self.new_value = value
        self.new_hour_class = hour_class
        self.new_is_rainy = is_rainy

        # output of predict class
        self.predict_class = None
    
    def fit(self):
        model = tf.keras.models.load_model(self.model_path)
        scaler = load(open(self.scaler_path, 'rb'))

        pc = PreparationClassification(queryset=self.queryset,
                                       value=self.new_value,
                                       hour_class=self.new_hour_class,
                                       is_rainy=self.new_is_rainy,
                                       window=18)
        pc.fit()
        dt = pc.data_ready
        dt[dt.columns] = scaler.transform(dt[dt.columns])
        feature = dt.values

        predict_class = model.predict(feature)

        # decode onehot
        predict_class = predict_class.argmax()
        self.predict_class = 'Error' if predict_class == 0 else 'Good' if predict_class == 1 else 'Suspect'
