from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)

from app.services.user_service import (
    get_users,
    get_user_by_id,
    get_user_by_email,
    create_user,
    update_user,
    patch_user,
    delete_user,
    get_users_by_role,
    get_active_users,
    get_users_ordered_by_name,
    get_users_ordered_by_date
)

router = APIRouter(
    tags=["Users"]
)


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar usuarios"
)
def list_users(
    db: Session = Depends(get_db)
):
    return get_users(db)


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar usuarios"
)
def list_users(
    role: str = None,
    is_active: bool = None,
    order_by: str = None,
    db: Session = Depends(get_db)
):

    if role:
        return get_users_by_role(
            db,
            role
        )

    if is_active is not None:
        return get_active_users(
            db,
            is_active
        )

    if order_by == "name":
        return get_users_ordered_by_name(
            db
        )

    if order_by == "date":
        return get_users_ordered_by_date(
            db
        )

    return get_users(db)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario"
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )

    return create_user(
        db,
        user_data
    )


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo"
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return update_user(
        db,
        user,
        user_data
    )


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente"
)
def patch_existing_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db)
):

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron campos para actualizar"
        )

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return patch_user(
        db,
        user,
        update_data
    )


@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    delete_user(
        db,
        user
    )

    return {"detail": "Usuario eliminado exitosamente"}
