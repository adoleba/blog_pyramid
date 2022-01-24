"""Pyramid bootstrap environment. """
from alembic import context
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config

from blog_pyramid.models.meta import Base

config = context.config

setup_logging(config.config_file_name)

settings = get_appsettings(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(url=settings['sqlalchemy.url'])
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = engine_from_config(
                config.get_section(config.config_ini_section), prefix='sqlalchemy.')

    with engine.connect() as connection:
        context.configure(
                    connection=connection,
                    target_metadata=target_metadata
                    )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
