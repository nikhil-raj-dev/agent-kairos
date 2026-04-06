from app.database.queries import get_product_sales, store_forecast
from app.utils.data_preprocessing import prepare_timeseries, impute_data
from app.models.forecasting_models import generate_forecast


def forecast_product(product_name : str, forecast_periods : int = 30):
    
    df = get_product_sales(product_name)
    df = impute_data(df)
    df = prepare_timeseries(df)

    forecast_df = generate_forecast(df, periods=forecast_periods)
    store_forecast(product_name, forecast_df)

    return forecast_df