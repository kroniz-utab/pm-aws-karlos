from django_pandas.io import read_frame
import pandas as pd

class PreparationClassification:
    def __init__(self,
                 queryset=None,
                 value=None,
                 hour_class=None,
                 is_rainy=None,
                 window=6):
        self.queryset = queryset
        self.window = window
        
        self.value = value
        self.hour_class = hour_class
        self.is_rainy = is_rainy

        self.data_ready = self.fit()

    def sequence_maker(self, dataframe, window=6, dropna=True):
        df = dataframe.copy()
        target = df.columns[0]
        window = window - 1

        for i in range(1, window + 1):
            df[f'{target}{i}'] = df[target].shift(i)

        if dropna:
            df = df.dropna()
        else:
            df = df.fillna(0)
        
        # recreate dataframe that can handle right sequence
        result = df[[f'{target}{i}' for i in range(window, 0, -1)]]
        result.loc[:, target] = df.loc[:, target]
        result.loc[:, 'hour_class'] = df.loc[:,'hour_class']
        result.loc[:, 'is_rainy'] = df.loc[:, 'is_rainy']
        result = result.tail(1)

        return result
    
    def fit(self):
        # create dataframe from queryset
        df = read_frame(self.queryset, fieldnames=['value', 'hour_class', 'is_rainy'])
        new_dataloc = df.shape[0] + 1
        df.loc[new_dataloc, 'value'] = self.new_value
        df.loc[new_dataloc, 'hour_class'] = self.new_hour_class
        df.loc[new_dataloc, 'is_rainy'] = self.new_is_rainy 
        return self.sequence_maker(df, window=self.window, dropna=True)

class PreparationPrediction:
    def __init__(self, value, queryset=None, lookback=72):
        self.new_value = value
        self.queryset = queryset
        self.lookback = lookback
        self.data_ready = self.fit()

    def fit(self):
        df = read_frame(self.queryset, fieldnames=['value', 'hour_class', 'is_rainy'])
        new_dataloc = df.shape[0] + 1
        df.loc[new_dataloc, 'value'] = self.new_value
        dataout = df.tail(self.lookback)
        return dataout['value'].to_numpy()

class PreparationPredictive:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.result = self.sequence_maker(self.dataframe, window=18, dropna=True)
    
    def sequence_maker(self, dataframe, window=6, dropna=True):
        df = dataframe.copy()
        target = df.columns[0]
        window = window - 1

        for i in range(1, window + 1):
            df[f'{target}{i}'] = df[target].shift(i)

        if dropna:
            df = df.dropna()
        else:
            df = df.fillna(0)
        
        # recreate dataframe that can handle right sequence
        result = df[[f'{target}{i}' for i in range(window, 0, -1)]]
        result.loc[:, target] = df.loc[:, target]
        result.loc[:, 'hour_class'] = df.loc[:,'hour_class']
        result.loc[:, 'is_rainy'] = df.loc[:, 'is_rainy']
        result = result.tail(1)

        return result