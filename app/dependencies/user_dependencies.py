from fastapi import HTTPException, Header


def get_user_or_404(user_id: int):
    """
    Dependencia para buscar un usuario por ID.
    """

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


def verify_token(
    x_token: str = Header(...)
):
    """
    Simulación de autenticación mediante cabecera.
    """

    if x_token != "device123":
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return x_token


def get_api_settings():
    """
    Configuración general de la API.
    """

    return {
        "app_name": "device_systems",
        "version": "2.0.0"
    }
