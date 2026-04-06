import numpy as np
import pandas as pd

def detect_anomalies(df, column='value', threshold=3):
    df = df.copy()
    
    mean = df[column].mean()
    std = df[column].std()

    if std == 0 or pd.isna(std):
        df["z_score"] = 0.0
        df["anomaly"] = False
        return df
    
    df['z_score'] = (df[column] - mean) / std
    df['anomaly'] = np.abs(df['z_score']) > threshold
    
    
    
    return df