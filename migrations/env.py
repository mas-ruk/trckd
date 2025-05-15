import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

from app import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    """
    Function to return the SQLAlchemy engine from the Flask application context.
    This handles both Flask-SQLAlchemy <3 and Flask-SQLAlchemy >=3.
    """
    try:
        # Flask-SQLAlchemy <3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Flask-SQLAlchemy >=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    """
    Function to return the database URL as a string, safely escaping any percent signs.
    """
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# Set the SQLAlchemy URL dynamically in the Alembic config
config.set_main_option('sqlalchemy.url', get_engine_url())

# target_metadata should point to the metadata of your models
# Make sure that your models are imported before this runs (e.g., by importing them in the app)
target_db = current_app.extensions['migrate'].db


def get_metadata():
    """
    Function to return the metadata object for the database.
    If Flask-SQLAlchemy has multiple metadata objects, we return the default.
    """
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """
    Function to run migrations in 'offline' mode.
    This configures the context with just a URL, without needing a live database connection.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Function to run migrations in 'online' mode.
    This involves creating an Engine and associating a connection with the Alembic context.
    """
    # This callback prevents an auto-migration from being generated if no schema changes are detected
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# Run migrations based on the mode (offline or online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
