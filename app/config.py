import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.orm import DeclarativeBase

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(dotenv_path=BASE_DIR / '.env')

token_api_telegram = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG")

# Redis config
name_redis = os.getenv("REDIS_NAME")
password_redis = os.getenv("REDIS_PASSWORD")
port_redis = os.getenv("REDIS_PORT")
host_redis = os.getenv("REDIS_HOST")

name_postgres = os.getenv("POSTGRES_NAME")
user_postgres = os.getenv("POSTGRES_USER")
password_postgres = os.getenv("POSTGRES_PASSWORD")
port_postgres = os.getenv("POSTGRES_PORT")
host_postgres = os.getenv("POSTGRES_HOST")

password_for_admin = os.getenv("PASSWORD_FOR_ADMIN")

redis_url = f'redis://{name_redis}:{password_redis}@{host_redis}:{port_redis}/0'
postgres_url = f"postgresql+asyncpg://{user_postgres}:{password_postgres}@{host_postgres}:{port_postgres}/{name_postgres}"


# Database

class Base(DeclarativeBase):
    ...
