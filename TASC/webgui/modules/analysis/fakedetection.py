import joblib
from sklearn import preprocessing
import pandas as pd

def SupeciousDetection():
    joblib_file = "joblib_RL_Model.pkl" 
    joblib_LR_model = joblib.load(joblib_file)
    data=  {
        'statuses_count':['240'],
        'followers_count':['25420'],
        'friends_count':['2424'],
        'favourites_count':['3563'],
        'listed_count':['0'],
        'sex_code':['0'],
        'lang_code':['1']

    }
    df = pd.DataFrame (data, columns = ['statuses_count','followers_count','friends_count','favourites_count','listed_count','sex_code','lang_code'])
    raw = preprocessing.scale(df)
    result=joblib_LR_model.best_estimator_.predict_proba(raw)
    lol = list(result[0])
    sup = {}
    sup['notsuspecious'] = lol[0]
    return sup
