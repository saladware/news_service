from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.config import DB_PSWD, DB_HOST, DB_NAME, DB_USER, DB_PORT
from app.database import Base


config = context.config

config.set_section_option(config.config_ini_section, 'DB_USER', DB_USER)
config.set_section_option(config.config_ini_section, 'DB_PSWD', DB_PSWD)
config.set_section_option(config.config_ini_section, 'DB_HOST', DB_HOST)
config.set_section_option(config.config_ini_section, 'DB_PORT', str(DB_PORT))
config.set_section_option(config.config_ini_section, 'DB_NAME', DB_NAME)


if config.config_file_name is not None:  # noqa
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
