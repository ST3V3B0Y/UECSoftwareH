from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app import create_app, db  # Importar la app Flask y la instancia de la base de datos
from app.models.historial import Historial  # Importar los modelos que usas
from app.models.usuario import Usuario  # Asegúrate de importar otros modelos como 'Usuario' si es necesario
from app.models.facultad import Facultad
from app.models.equipo import Equipo

# Configuración de Alembic
config = context.config

# Configuración del archivo de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establecer los metadatos de los modelos de SQLAlchemy
target_metadata = db.metadata  # Aquí se toman los metadatos de los modelos

def run_migrations_offline() -> None:
    """Correr migraciones en modo 'offline'."""

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
    """Correr migraciones en modo 'online'."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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