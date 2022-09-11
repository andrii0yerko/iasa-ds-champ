import pandas as pd
from feature_engine.creation import CyclicalFeatures
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from constants import *


def load_data(path):
    df = pd.read_csv(path)
    df[CATEGORY_COL] = df[CATEGORY_COL].astype('category')

    for x in DATE_COL:
        df[x] = pd.to_datetime(df[x])

    df = df.sort_values(by='install_date')

    features = df[[x for x in df.columns if x not in TARGET_COL]]
    
    return features


def generate_date_features(df):
    df[['install_year', 'install_month', 'install_day']] = df['install_date'].astype(str).str.split('-', expand=True).astype(int)
    
    cyclical = CyclicalFeatures(variables=None, drop_original=True)
    sin_cos_features = cyclical.fit_transform(df[['install_day', 'install_month', 'install_year']])
    df = pd.concat([df, sin_cos_features], axis=1)
    
    df['day_of_week'] = df['install_date'].apply(lambda x: x.weekday())
    
    usb = CustomBusinessDay(calendar = USFederalHolidayCalendar())
    non_holidays = list(pd.date_range('2021-12-01', '2022-01-31', freq=usb))
    df['installed_on_holiday'] = df['install_date'].apply(lambda x: False if x in non_holidays else True)
    
    install_date_users = df['install_date'].value_counts()
    df['users_joined_this_day'] = df['install_date'].apply(lambda x: install_date_users[x])
    
    return df


def count_delta_changes(df):
    def count_difference(cols, days, interval=1):
        for col in cols:
            for i in range(len(days)-1, interval-1, -interval):
                df[col+str(days[i])+'_delta'] = df[col+str(days[i])] - df[col+str(days[i-interval])]
    
    for cols, days in zip([daily_cols, ret_cols, sessions_cols, trg_daily_cols], [daily_days, ret_days, sessions_days, trg_daily_days]):
        count_difference(cols, days)
    
    return df


def process_data(features):
    features = features.copy()
    res = generate_date_features(count_delta_changes(features))
    return res.drop(DATE_COL, axis=1)


def add_lr_features(X, lr_models):
    for c in ['sub', 'iap', 'ad']:
        X[f'forecasted_{TS_TARGET[c]}'] = lr_models[c].predict(X[TS_COLS[c]])

    