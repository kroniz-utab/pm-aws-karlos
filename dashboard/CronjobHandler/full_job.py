# for offline test
import pandas as pd
from .new_save import *
from .create_new import from_dataframe


def testing():
    data = pd.read_csv('data/data_januari.csv')
    data = data.reset_index(drop=True)
    for i in range(len(data)):
        aws_count = AwsData.objects.count()
        awstime, temp, rh, pa, sr, ws, wd, ch = from_dataframe(data, i)
        if aws_count < 18:
            no_all(awstime, temp, rh, pa, sr, ws, wd, ch, is_rainy=1)
        elif aws_count < 144 and aws_count >= 18:
            just_class(awstime, temp, rh, pa, sr, ws, wd, ch, is_rainy=1)
        else:
            full_system(awstime, temp, rh, pa, sr, ws, wd, ch, is_rainy=1)
    
