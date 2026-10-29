#!/bin/env python3

from logging.config import fileConfig
import os
from pathlib import Path
import sys
from typing import Any

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.config.config import config as app_config
from modules.database.database_utils import database_utils
from modules.database.schema import Base


alembic_config = context.config
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = Base.metadata


def _database_url() -> str:
    '''Resolve the configured database URL, allowing explicit test overrides.'''
    override_url = alembic_config.attributes.get("database_url")
    if isinstance(override_url, str):
        return override_url
    environment_url = os.environ.get("WGDASHBOARD_DATABASE_URL")
    if environment_url:
        return environment_url

    config_loaded, config_data = app_config.read()
    if not config_loaded:
        raise RuntimeError("failed to read the WGDashboard configuration")

    database_config_found, database_config = app_config.filter(config_data, "DATABASE")
    if not database_config_found:
        raise RuntimeError("the DATABASE configuration section is missing")

    url_created, connection_url = database_utils.generate_connection_string(database_config)
    if not url_created:
        raise RuntimeError("failed to create the database URL from configuration")

    return connection_url


def run_migrations_offline() -> None:
    '''Run migrations without creating a database connection.'''
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    '''Run migrations using the configured engine or injected connection.'''
    supplied_connection: Any = alembic_config.attributes.get("connection")
    if supplied_connection is not None:
        _run_migrations(supplied_connection)
        return

    connection_url = _database_url()
    alembic_config.set_main_option("sqlalchemy.url", connection_url.replace("%", "%%"))
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        _run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
