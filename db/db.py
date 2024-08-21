from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+aiomysql://TodoApp:password@localhost/TodoApp"

async_engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session