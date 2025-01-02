from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve the database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.environ.get("BUDGETA_DB_URL")

# Create the async database engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Create an async sessionmaker
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Function to initialize the database
async def init_db():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency to get an async database session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
