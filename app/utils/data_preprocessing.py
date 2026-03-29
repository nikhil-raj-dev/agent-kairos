import pandas as pd

def prepare_timeseries(df):
    
    df = df.copy()

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    return df


def impute_data(df):
    
    if df.empty:
        return df
    df = df.copy()
    df = df.set_index('date')

    if df.index.min() is pd.NaT or df.index.max() is pd.NaT:
        return df

    data_index_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(data_index_range)

    df['value'] = df['value'].interpolate(method='time')
    df = df.reset_index().rename(columns={'index': 'date'})

    return df
