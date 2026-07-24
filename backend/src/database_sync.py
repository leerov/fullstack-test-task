from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

# Convert asyncpg URL to psycopg2 URL for synchronous operations in Celery
sync_db_url = settings.db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

sync_engine = create_engine(sync_db_url)
sync_session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)