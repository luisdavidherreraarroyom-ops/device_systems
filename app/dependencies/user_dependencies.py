from fastapi import HTTPException, status, Header
from app.services import user_service

def get_user_or_404(user_id: int) -> dict:
    """Verifica que el usuario exista; si no, lanza 404 Not Found."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

def validate_unique_email(email: str, current_user_id: int = None):
    """Verifica que un correo no esté registrado por otro usuario."""
    existing_user = user_service.get_user_by_email(email)
    if existing_user and (current_user_id is None or existing_user["id"] != current_user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{email}' ya se encuentra registrado"
        )

def verify_custom_header(x_api_token: str = Header(None, description="Header de autenticación opcional")):
    """Simulación de autenticación básica vía header."""
    if x_api_token and x_api_token != "secret-pass":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de cabecera inválido"
        )
    return x_api_token