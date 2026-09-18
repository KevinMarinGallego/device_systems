device_systems
Descripción

device_systems es una API REST desarrollada con FastAPI para la gestión de usuarios del sistema.

La aplicación permite:

Crear usuarios.
Consultar usuarios.
Listar usuarios.
Filtrar usuarios por rol.
Filtrar usuarios por estado.
Actualizar usuarios completamente.
Actualizar usuarios parcialmente.
Eliminar usuarios.
Validar datos mediante Pydantic.
Persistir información usando SQLite.
Documentar automáticamente la API con Swagger y ReDoc.
Tecnologías utilizadas
Python 3.14
FastAPI
SQLAlchemy
SQLite
Pydantic
Uvicorn

# Device Management System

## Tecnologías

- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic

## Funcionalidades

### Usuarios
- Crear
- Listar
- Actualizar
- Eliminar

### Dispositivos
- Crear
- Listar
- Actualizar
- Eliminar

### Préstamos
- Crear préstamo
- Devolver préstamo
- Consultar historial

### Consultas avanzadas
- /loans/details
- /users/{user_id}/loans
- /devices/{device_id}/loans
- filtros por estado
- filtros por correo
- filtros por tipo de dispositivo