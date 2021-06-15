import tensorflow as tf
import pandas as pd
import numpy as np
from pickle import load
from .DataPrepHandler import *

def class_predict(value, awsTime, is_rainy, 
                  model_path=None, scaler_path=None, queryset=None):
    
    model = tf.keras.models.load_model(model_path)
    scaler = load(open(scaler_path, 'rb'))

    # create series time
    dtime = pd.Series(awsTime)
    dtime = pd.to_datetime(dtime)
    hour_class = dtime.dt.hour
    
    df = from_queryset(queryset, value, hour_class, is_rainy)
    df = sequence_maker(df, window=18)
    df = df.tail(1)

    df[df.columns] = scaler.transform(df[df.columns])

    predict_class = model.predict(df)
    predict_class = np.argmax(predict_class)

    cls = 'Error' if predict_class == 0 else 'Good' if predict_class == 1 else 'Suspect'
    return cls

