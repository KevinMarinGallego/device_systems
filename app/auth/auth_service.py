from sqlalchemy.orm import Session

from app.models.user_model import User

from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token
)


def register_user(
    db: Session,
    user_data
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == user_data.email
        )
        .first()
    )

    if existing_user:
        return None

    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(
            user_data.password
        ),
        role=user_data.role,
        is_active=True
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def login_user(
    db: Session,
    username: str,
    password: str
):

    user = (
        db.query(User)
        .filter(
            User.email == username
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }