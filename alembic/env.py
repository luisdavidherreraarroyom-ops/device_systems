"""Configuración de Alembic para device_systems."""
# pylint: disable=wrong-import-position,unused-import,no-member
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Agregar la raíz del proyecto al path de Python para poder importar 'app'
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Importar Base y los modelos para que Alembic detecte las tablas al autogenerar
from app.database.connection import Base
import app.models.user_model
import app.models.device_model
import app.models.loan_model

# Configuración de Alembic desde el archivo .ini
config = getattr(context, "config", None)
if config is None:
    raise RuntimeError("Alembic no proporcionó la configuración del contexto")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de nuestros modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Modo offline: genera scripts de migración sin conectarse a la base."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        getattr(context, "run_migrations")()


def run_migrations_online() -> None:
    """Modo online: ejecuta las migraciones directamente en la base de datos."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            compare_type=True,
        )

        with context.begin_transaction():
            getattr(context, "run_migrations")()


if getattr(context, "is_offline_mode")():
    run_migrations_offline()
else:
    run_migrations_online()