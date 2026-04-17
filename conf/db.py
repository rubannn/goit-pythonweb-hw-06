import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
pg_port = os.getenv('POSTGRES_PORT')
pg_db = os.getenv('POSTGRES_DB')

DB_URL = f"postgresql+psycopg2://{user}:{password}@localhost:{pg_port}/{pg_db}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
