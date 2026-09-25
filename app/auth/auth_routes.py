from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    UserRegister,
    UserResponse,
    UserLogin,
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
def register(
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
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    token = login_user(
        db,
        user_data.email,
        user_data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    return token


from fastapi import Header

@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user = Depends(
        get_current_user
    )
):

    return current_user