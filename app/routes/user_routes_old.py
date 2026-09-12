from operator import index
from fastapi import APIRouter, HTTPException, Response
from app.schemas.user_schema import User, UserCreate, UserResponse
from app.schemas.user_schema import UserUpdate
# from fastapi import Depends
# from app.dependencies.database_dependency import (
#     get_user_or_404,
#     verify_token
# )


router = APIRouter()

# Base de datos temporal
users = [
    User(
        id=1,
        name="kevin",
        email="kevin@gmail.com",
        role="admin",
        is_active=True
    ),
    User(
        id=2,
        name="carlos",
        email="carlos@gmail.com",
        role="user",
        is_active=False
    )
]


# GET /users
# Lista todos los usuarios y permite filtrar
@router.get(
    "/users",
    tags=["Users"],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios registrados",
    response_description="Lista de usuarios"
)
def get_users(
    response: Response,
    role: str = None,
    is_active: bool = None
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    result = users

    if role:
        result = [
            user for user in result
            if user.role == role
        ]

    if is_active is not None:
        result = [
            user for user in result
            if user.is_active == is_active
        ]

    return result


# GET /users/{user_id}
# Busca un usuario por ID
@router.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: int):

    for user in users:
        if user.id == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# POST /users
# Crear usuario nuevo
@router.post(
    "/users",
    tags=["Users"],
    summary="Crear usuario",
    description="Registra un nuevo usuario",
    response_description="Usuario creado"
)
def create_user(user: UserCreate):

    # Validar correo duplicado
    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    # Crear nuevo usuario
    new_user = User(
        id=len(users) + 1,
        **user.model_dump()
    )

    users.append(new_user)

    return new_user

@router.put(
    # PUT
    
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(user_id: int, user_data: UserCreate):

    for index, user in enumerate(users):
        if user.id == user_id:
            updated_user = User(
                id=user_id,
                **user_data.model_dump()
            )
            users[index] = updated_user 
            return updated_user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
@router.patch(
    # PATCH
    "/users/{user_id}",
    response_model=UserResponse
)
def patch_user(
    user_id: int,
    user_data: UserUpdate
):
    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron campos para actualizar"
        )
    for index, user in enumerate(users):
        if user.id == user_id:
            updated_user = user.model_copy(
                update=update_data
            )
            users[index] = updated_user
            return updated_user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@router.delete("/users/{user_id}")
# DELETE

def delete_user(user_id: int):

    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {
                "message":
                "Usuario eliminado correctamente"
            }
    raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
    )
    