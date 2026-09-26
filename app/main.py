from fastapi import FastAPI
from app.routes.user_routes import router
from app.database.connection import Base
from app.database.connection import engine
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.request_middleware import (
    request_middleware
)
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


from app.models.user_model import User
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios, dispositivos y prestamos",
    version="3.0.0",
    contact={
        "name": "kevin marin",
        "email": "kevin@gmail.com"
    }
)


app.include_router(
    auth_router
)

app.include_router(router)
app.include_router(device_router)
app.include_router(loan_router)

app.middleware("http")(
    request_middleware
)

app.state.limiter = limiter
app.add_middleware(
    SlowAPIMiddleware
)