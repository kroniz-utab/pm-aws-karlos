import tensorflow as tf
import pandas as pd
import numpy as np
from pickle import load

def predict_lstm(model, series, window_size=72):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w : w.batch(window_size))
    ds = ds.batch(16).prefetch(1)
    forecast = model.predict(ds)
    forecast = forecast[0].reshape((-1))
    return forecast 