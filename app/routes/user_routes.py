from fastapi import APIRouter, HTTPException, Response
from app.schemas.user_schema import User, UserCreate, UserResponse

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
    response_model=list[UserResponse]
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
    response_model=UserResponse
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