import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

logger = logging.getLogger(__name__)

# Global variables for database
engine: object | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


async def init_database():
    """Initialize database connection if DATABASE_URL is provided."""
    global engine, async_session

    if not settings.database_url:
        logger.info("No DATABASE_URL provided, running without database")
        return

    try:
        engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_recycle=300,
        )

        async_session = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        logger.info("Database connection initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_database() -> AsyncSession | None:
    """Get database session."""
    if not async_session:
        yield None
        return

    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_health() -> bool:
    """Check if database is accessible."""
    if not engine:
        return True  # No database configured, consider healthy

    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
