from fastapi import FastAPI
from app.routes.user_routes import router
from app.database.connection import Base
from app.database.connection import engine
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

from app.models.user_model import User
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios",
    version="3.0.0",
    contact={
        "name": "kevin marin",
        "email": "kevin@gmail.com"
    }
)

app.include_router(router)
app.include_router(device_router)
app.include_router(loan_router)