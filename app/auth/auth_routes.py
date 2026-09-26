from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from app.core.limiter import limiter

from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    UserRegister,
    UserResponse,
    Token
)

from app.auth.auth_service import (
    register_user,
    login_user
)

from app.dependencies.database_dependency import (
    get_db
)

from app.dependencies.auth_dependency import (
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    user = register_user(
        db,
        user_data
    )

    if not user:

        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )

    return user


@router.post(
    "/login",
    response_model=Token
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    token = login_user(
        db,
        form_data.username,
        form_data.password
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    return token


@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user=Depends(
        get_current_user
    )
):

    return current_user