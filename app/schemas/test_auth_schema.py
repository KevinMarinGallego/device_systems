from app.schemas.auth_schema import UserRegister

user = UserRegister(
    name="Carlos",
    email="carlos@gmail.com",
    password="Carlos123",
    role="admin"
)

print(user)
