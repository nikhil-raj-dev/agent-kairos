import plotly.graph_objects as go
import pandas as pd


def plot_sales_history(df):

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    fig = go.Figure()

    fig.add_trace(
        go.Line(x=df["date"].astype(str).tolist(), 
                   y=df["value"].tolist(), 
                   mode="lines", 
                   name="Sales"
        )
    )

    fig.update_layout(title="Sales History", xaxis_title="Date", yaxis_title="Value")

    return fig


def plot_forecast(df, forecast_df, forecast_periods=30):
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    fig = go.Figure()

    fig.add_trace(
        go.Line(x=df["date"].astype(str).tolist(), 
                   y=df["value"].tolist(), 
                   mode="lines", 
                   name="Actual"
        )
    )

    fig.add_trace(
        go.Line(x=forecast_df["date"][-forecast_periods:].astype(str).tolist(), 
                   y=forecast_df["forecast"][-forecast_periods:].tolist(), 
                   mode="lines", 
                   name="Forecast"
        )
    )

    fig.update_layout(title="Forecast vs Actual", xaxis_title="Date", yaxis_title="Value")

    return fig


def plot_anomalies(df):

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    fig = go.Figure()

    normal = df[df["anomaly"] == False]
    anomaly = df[df["anomaly"] == True]

    fig.add_trace(
        go.Scatter(x=df["date"].astype(str).tolist(), 
                   y=df["value"].tolist(), 
                   mode="lines", 
                   name="Normal"
        )
    )

    fig.add_trace(
        go.Scatter(x=anomaly["date"].astype(str).tolist(), 
                   y=anomaly["value"].tolist(), 
                   mode="markers", 
                   name="Anomalies", 
                   marker=dict(color="red", size=8)
        )
    )

    fig.update_layout(title="Anomaly Detection", xaxis_title="Date", yaxis_title="Value")

    return fig