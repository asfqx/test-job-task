from .database import engine
from .database import Base


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
