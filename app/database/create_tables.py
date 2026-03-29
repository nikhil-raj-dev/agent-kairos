import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from sqlalchemy import text
from app.database.db_connection import get_engine

engine = get_engine()


def create_tables():

    with engine.connect() as connection:

        # Sales Data Table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS sales_data (
                date DATE,
                product VARCHAR(50),
                value FLOAT
            );
        """))

        # Forecast Table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS forecast_table (
                product VARCHAR(50),
                date DATE,
                forecast FLOAT,
                ingestion_timestamp TIMESTAMP
            );
        """))

        # Index (performance)
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_product_date
            ON sales_data (product, date);
        """))

        connection.commit()

    print("Tables created successfully!")


def load_csv_data():

    file_path = ROOT_DIR / "data" / "sales_data.csv"

    if not file_path.exists():
        print("CSV file not found. Skipping data load.")
        return

    df = pd.read_csv(file_path)

    print(f"📊 Loading {len(df)} rows into sales_data...")

    # Ensure correct column names
    df = df[['date', 'product', 'value']]

    with engine.connect() as connection:
        df.to_sql(
            "sales_data",
            con=connection,
            if_exists="append",
            index=False
        )

    print("Data loaded successfully!")


if __name__ == "__main__":
    create_tables()
    load_csv_data()
