from app.auth.security import (
    get_password_hash,
    verify_password
)

password = "Carlos123"

hashed = get_password_hash(
    password
)

print(
    "HASH:",
    hashed
)

print(
    verify_password(
        password,
        hashed
    )
)