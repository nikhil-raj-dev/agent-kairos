from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_PORT = os.getenv("DB_PORT")

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)

def get_engine():
    return create_engine(
        os.getenv("DATABASE_URL"),
        connect_args={"sslmode": "require"}  # 🔥 important for Render
    )

# def get_engine():
#     return engine
