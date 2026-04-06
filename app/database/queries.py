import pandas as pd
from datetime import datetime

from app.database.db_connection import get_engine

engine = get_engine()


def get_all_products():
    sql_query = "SELECT DISTINCT product FROM sales_data"
    
    with engine.connect() as connection:
        df = pd.read_sql(sql_query, connection)
    
    return df['product'].tolist()


def get_product_sales(product_name):
    sql_query = f"""Select date, value from sales_data where product = '{product_name}' order by date"""
    
    with engine.connect() as connection:
        df = pd.read_sql(sql_query, connection)
    
    return df


def get_last_n_days_sales(product_name, n_days):
    sql_query = f"""
        SELECT date, value
        FROM (
            SELECT date, value
            FROM sales_data
            WHERE product = '{product_name}'
            ORDER BY date DESC
            LIMIT {n_days}
        ) recent
        ORDER BY date ASC
    """
    with engine.connect() as connection:
        df = pd.read_sql(sql_query, connection)

    return df


def store_forecast(product_name, forecast_df):
    forecast_df['product'] = product_name
    forecast_df['ingestion_timestamp'] = datetime.now()

    columns_order = ['product','date', 'forecast', 'ingestion_timestamp']
    forecast_df = forecast_df[columns_order]

    with engine.connect() as connection:
        forecast_df.to_sql('forecast_table', con=connection, if_exists='append', index=False)

    return True