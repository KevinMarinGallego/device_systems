from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./device_systems.db"

# Motor de base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False, # Control manual de transacciones
    autoflush=False, # Control manual de sincronización
    bind=engine # Vincula al motor de base de datos
)

Base = declarative_base()