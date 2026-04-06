from app.database.queries import get_product_sales
from app.utils.data_preprocessing import prepare_timeseries, impute_data
from app.models.anomaly_detection import detect_anomalies


def detect_product_anomalies(product_name : str):
    
    df = get_product_sales(product_name)
    df = prepare_timeseries(df)
    df = impute_data(df)
    df = prepare_timeseries(df)

    anomaly_df = detect_anomalies(df)

    return anomaly_df