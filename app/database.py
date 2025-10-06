from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base



Base = declarative_base()
DATABASE_URL = "sqlite+aiosqlite:///./users.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, 
                                 class_=AsyncSession, 
                                 expire_on_commit=False
)

from . import models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
