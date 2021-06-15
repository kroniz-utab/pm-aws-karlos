from django_pandas.io import read_frame

def sequence_maker(dataframe, window=18, dropna=True):
    df = dataframe.copy()
    target = df.columns[0]
    window = window - 1

    for i in range(1, window + 1):
        df[f'{target}{i}'] = df[target].shift(i)
    
    if dropna:
        df = df.dropna()
    else:
        df=df.fillna(0)
    
    result = df[[f'{target}{i}' for i in range(window, 0, -1)]]
    result.loc[:, target] = df.loc[:, target]
    result.loc[:, 'hour_class'] = df.loc[:,'hour_class']
    result.loc[:, 'is_rainy'] = df.loc[:, 'is_rainy']

    return result


def from_queryset(queryset, value, hour_class, is_rainy):
    df = read_frame(queryset, fieldnames=['value', 'hour_class', 'is_rainy'])
    new_dataloc = df.shape[0] + 1
    df.loc[new_dataloc, 'value'] = value
    df.loc[new_dataloc, 'hour_class'] = hour_class
    df.loc[new_dataloc, 'is_rainy'] = is_rainy

    return df