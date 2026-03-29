from app.database.queries import get_product_sales, get_last_n_days_sales
from app.utils.data_preprocessing import prepare_timeseries, impute_data

def get_data(product_name : str, n_days : int = 90):
    
    if not product_name:
        raise ValueError("Product is required")
    
    df = get_product_sales(product_name)

    if df.empty:
        raise ValueError(f"No data found for product: {product_name}")
    
    df = prepare_timeseries(df)
    df = impute_data(df)

    return df