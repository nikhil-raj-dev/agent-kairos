import plotly.graph_objects as go


def plot_sales_history(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df["date"], y=df["value"], mode="lines", name="Sales"
        )
    )

    fig.update_layout(title="Sales History", xaxis_title="Date", yaxis_title="Value")

    return fig


def plot_forecast(df, forecast_df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df["date"], y=df["value"], mode="lines", name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(x=forecast_df["date"][-30:], y=forecast_df["forecast"][-30:], mode="lines", name="Forecast"
        )
    )

    fig.update_layout(title="Forecast vs Actual", xaxis_title="Date", yaxis_title="Value")

    return fig


def plot_anomalies(df):
    fig = go.Figure()

    normal = df[df["anomaly"] == False]
    anomaly = df[df["anomaly"] == True]

    fig.add_trace(
        go.Scatter(x=normal["date"], y=normal["value"], mode="lines", name="Normal"
        )
    )

    fig.add_trace(
        go.Scatter(x=anomaly["date"], y=anomaly["value"], mode="markers", name="Anomalies"
        )
    )

    fig.update_layout(title="Anomaly Detection", xaxis_title="Date", yaxis_title="Value")

    return fig