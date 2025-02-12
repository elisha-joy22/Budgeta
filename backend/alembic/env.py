from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from alembic import context
from app.models.invitees import Invitee
from app.models.events import Event, EventGroup
from app.models.user import User
from app.models.checklists import Checklist,ChecklistItem

# Alembic Config object, providing access to values in alembic.ini
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Link SQLModel metadata to Alembic's target metadata
target_metadata = SQLModel.metadata


# Include only specific tables
included_tables = {"invitee"}

def include_name(name, type_, parent_names):
    """Filter table names during migrations."""
    return name in included_tables if type_ == "table" else True

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    Configures the context with just a URL and no Engine.
    Calls to context.execute() will emit the generated SQL to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,  # Apply table filtering
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this mode, an Engine is created and a connection is associated with the context.
    """
    # Use synchronous PostgreSQL engine (psycopg2) here
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=include_name,  # Apply table filtering
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
