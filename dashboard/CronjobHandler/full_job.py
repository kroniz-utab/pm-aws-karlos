# for offline test
import pandas as pd
from .new_save import *
from .create_new import from_dataframe


def testing():
    data = pd.read_csv('data/data_januari.csv')
    idx = AwsData.objects.count()
    awstime, temp, rh, pa, sr, ws, wd, ch = from_dataframe(data, idx)
    if idx < 18:
        no_all(awstime, temp, rh, pa, sr, ws, wd, ch, is_rainy=1)
    elif idx < 144 and idx >= 18:
        just_class(awstime, temp, rh, pa, sr, ws, wd, ch, is_rainy=1)
    else:
        full_system(awstime, temp, rh, pa, sr, ws, wd, ch, is_rainy=1)
