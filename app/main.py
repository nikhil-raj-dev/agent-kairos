from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent.agent import run_agent
from app.tools.data_tool import get_data
from app.tools.forecast_tool import forecast_product
from app.tools.anomaly_tool import detect_product_anomalies
from app.tools.visualization_tool import plot_sales_history, plot_forecast, plot_anomalies

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str


@app.post("/chat")
def chat_endpoint(request: Query):

    query = request.query

    response = run_agent(query)

    response_text = response["response"]
    tool_used = response["tool_used"]
    tool_args = response["tool_args"]

    chart_json = None

    if tool_used == "forecast_product":
        product = tool_args.get("product_name")
        print(f"###################################################: {product}")
        df = get_data(product)
        forecast_df = forecast_product(product, 30)
        fig = plot_forecast(df, forecast_df)
        chart_json = fig.to_json()

    elif tool_used == "get_data":
        product = tool_args.get("product_name")
        df = get_data(product)
        fig = plot_sales_history(df)
        chart_json = fig.to_json()

    elif tool_used == "detect_product_anomalies":
        product = tool_args.get("product_name")
        df = detect_product_anomalies(product)
        fig = plot_anomalies(df)
        chart_json = fig.to_json()

    return {
        "response": response["response"],
        "chart": chart_json,
        "logs": response["logs"]
    }