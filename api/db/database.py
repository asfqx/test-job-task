from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.config import settings

DATABASE_URL = settings.db_url
engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
