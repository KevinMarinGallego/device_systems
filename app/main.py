from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistemadevice_systems",
    version="1.0"
)

app.include_router(router)