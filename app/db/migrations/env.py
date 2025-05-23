import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))


# Imports from `app` should go after `path` patch
from app.core.settings import settings  # isort:skip
from app.db.declarative_base import Base  # isort:skip
from app.db.session import make_url_sync  # isort:skip

# Import models to make them visible by alembic
import app.db.models.users  # isort:skip
import app.db.models.chats  # isort:skip
import app.db.models.groups  # isort:skip
import app.db.models.messages  # isort:skip

postgres_dsn = make_url_sync(settings.POSTGRES_DSN)
context_config = context.config
fileConfig(context_config.config_file_name)
target_metadata = Base.metadata
context_config.set_main_option("sqlalchemy.url", postgres_dsn)


def run_migrations_online() -> None:
    connectable = engine_from_config(
        context_config.get_section(context_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
