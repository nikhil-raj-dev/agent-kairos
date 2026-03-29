import pandas as pd
from prophet import Prophet

def prepare_data_for_prophet(df):
    
    df = df.copy()
    df = df.rename(columns={'date': 'ds', 'value': 'y'})
    return df


def generate_forecast(df, periods=30):
    
    df = df.copy()
    df = df.sort_values('date')
    prophet_df = prepare_data_for_prophet(df)
    
    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    forecast_df = forecast[['ds', 'yhat']].rename(columns={'ds': 'date', 'yhat': 'forecast'})
    
    return forecast_df