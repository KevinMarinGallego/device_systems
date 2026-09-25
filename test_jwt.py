from app.auth.security import (
    create_access_token,
    decode_access_token
)

token = create_access_token(
    {
        "sub": "carlos@gmail.com"
    }
)

print("TOKEN:")
print(token)

print()

print("PAYLOAD:")
print(
    decode_access_token(
        token
    )
)