import asyncio
import logging
import sys
import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy.exc import SQLAlchemyError
from app.db import Base, engine
from app.models import Post

# Добавляем путь к папке app в sys.path, чтобы импорты работали правильно
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Это позволяет Alembic найти ваш Base и работать с моделями
target_metadata = Base.metadata

config = context.config

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.runtime.migration")


async def run_migrations_online():
    try:
        async with engine.begin() as connection:
            await connection.run_sync(do_run_migrations)
    except SQLAlchemyError as e:
        logger.error(f"Error running migrations online: {e}")
        raise


def do_run_migrations(connection):
    try:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        raise


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    try:
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()
    except Exception as e:
        logger.error(f"Error running migrations offline: {e}")
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
