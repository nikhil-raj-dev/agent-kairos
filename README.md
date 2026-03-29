# Agent-Kairos

Agent-Kairos is a full-stack AI analytics assistant for product sales data. It lets you ask natural-language questions and can:

- show historical sales
- forecast future sales
- detect anomalies
- render charts in a web UI

The backend uses FastAPI + tool-calling with an OpenAI-compatible client (configured for Groq), while the frontend is a lightweight HTML/CSS/JS app with Plotly visualizations.

## Features

- Natural-language query interface (`/chat` endpoint)
- Tool routing for:
  - `get_data`
  - `forecast_product`
  - `detect_product_anomalies`
- Forecasting with Prophet
- Z-score based anomaly detection
- Plotly chart rendering (history, forecast, anomalies)
- Chat-style UI with agent execution logs

## Tech Stack

- Backend: FastAPI, Uvicorn, Pandas, SQLAlchemy
- LLM client: `openai` SDK against Groq OpenAI-compatible endpoint
- Forecasting: Prophet
- Visualization: Plotly
- Frontend: Vanilla HTML/CSS/JS
- Database: PostgreSQL

## Project Structure

```text
agent-kairos/
├── app/
│   ├── main.py                      # FastAPI app and /chat endpoint
│   ├── agent/
│   │   ├── agent.py                 # LLM tool-calling orchestration
│   │   └── prompt.py                # System and explanation prompts
│   ├── database/
│   │   ├── db_connection.py         # SQLAlchemy engine setup
│   │   └── queries.py               # DB queries and forecast persistence
│   ├── models/
│   │   ├── forecasting_models.py    # Prophet forecast model
│   │   └── anomaly_detection.py     # Z-score anomaly detection
│   ├── tools/
│   │   ├── data_tool.py
│   │   ├── forecast_tool.py
│   │   ├── anomaly_tool.py
│   │   └── visualization_tool.py
│   └── utils/
│       └── data_preprocessing.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── data/
│   └── sales_data.csv               # Sample data (date, product, value)
├── tests/
│   └── test_agent.py                # Interactive CLI smoke script
└── requirements.txt
```

## Prerequisites

- Python 3.9+
- PostgreSQL
- Groq API key

## Installation

```bash
# 1) Create and activate environment
python -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the repo root:

```env
GROQ_API_KEY=your_groq_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=agent_kairos
DB_USER=postgres
DB_PASSWORD=postgres
```

## Database Setup

Create the required tables:

```sql
CREATE TABLE IF NOT EXISTS sales_data (
    date DATE NOT NULL,
    product TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS forecast_table (
    product TEXT NOT NULL,
    date DATE NOT NULL,
    forecast DOUBLE PRECISION NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL
);
```

Load sample data:

```bash
# Example with psql
\copy sales_data(date,product,value) FROM 'data/sales_data.csv' DELIMITER ',' CSV HEADER;
```

## Run the Application

### 1) Start backend

```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 2) Start frontend (from repo root)

```bash
python -m http.server 5500
```

Open: `http://127.0.0.1:5500/frontend/index.html`

## API

### `POST /chat`

Request:

```json
{
  "query": "Forecast next 30 days for product B"
}
```

Response shape:

```json
{
  "response": "...natural language explanation...",
  "chart": "{...plotly_json_or_null...}",
  "logs": [
    "Received query: ...",
    "Selected tool: ...",
    "Arguments: ...",
    "Executing tool...",
    "Tool execution complete"
  ]
}
```

## Example Queries

- `Show last 3 months sales for product A`
- `Forecast next 30 days for product B`
- `Detect anomalies in product C`

## How It Works

1. User sends a query to `/chat`.
2. `run_agent()` builds a system prompt with available products from DB.
3. LLM decides whether to call one of the registered tools.
4. Tool executes data/forecast/anomaly logic.
5. A second LLM pass generates a human explanation from tool output.
6. Backend returns explanation, logs, and optional Plotly chart JSON.

## Notes and Current Limitations

- Product names must match exactly (for example `A`, `B`, `C`).
- `get_data` exposes an `n_days` argument but currently fetches full history.
- `detect_product_anomalies` currently returns only anomaly rows.
- SQL queries are currently string-formatted; parameterized queries would be safer.
- `tests/test_agent.py` is an interactive script, not a pytest test suite.

## Next Improvements (Optional)

- Add proper pytest-based unit/integration tests.
- Add DB migrations and seed scripts.
- Parameterize SQL queries.
- Return both normal + anomaly points for richer anomaly charts.
- Add Docker setup for one-command local run.

