import numpy as np
import pandas as pd

def detect_anomalies(df, column='value', threshold=3):
    df = df.copy()
    
    mean = df[column].mean()
    std = df[column].std()
    
    df['z_score'] = (df[column] - mean) / std
    df['anomaly'] = np.abs(df['z_score']) > threshold
    
    anomalies_df = df[df['anomaly']].drop(columns=['z_score'])

    print(mean, std)
    print(df)
    
    return anomalies_df