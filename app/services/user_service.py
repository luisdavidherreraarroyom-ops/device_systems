from app.data.users_db import db_users
from app.schemas.user_schema import UserCreate, UserUpdatePartial
from typing import Optional

def get_all_users(role: Optional[str] = None, is_active: Optional[bool] = None) -> list[dict]:
    """Obtiene todos los usuarios con opción de filtrado por rol o estado."""
    result = db_users
    if role:
        result = [u for u in result if u["role"].lower() == role.lower()]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result

def get_user_by_id(user_id: int) -> Optional[dict]:
    """Busca un usuario por ID."""
    for user in db_users:
        if user["id"] == user_id:
            return user
    return None

def get_user_by_email(email: str) -> Optional[dict]:
    """Busca un usuario por correo electrónico."""
    for user in db_users:
        if user["email"].lower() == email.lower():
            return user
    return None

def create_user(user_data: UserCreate) -> dict:
    """Crea un usuario asignando un ID autoincremental."""
    new_id = max([u["id"] for u in db_users], default=0) + 1
    new_user = {
        "id": new_id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active
    }
    db_users.append(new_user)
    return new_user

def update_user_full(user_id: int, user_data: UserCreate) -> dict:
    """Reemplaza completamente la información de un usuario (PUT)."""
    user = get_user_by_id(user_id)
    if user:
        user["name"] = user_data.name
        user["email"] = user_data.email
        user["role"] = user_data.role
        user["is_active"] = user_data.is_active
    return user

def update_user_partial(user_id: int, user_data: UserUpdatePartial) -> dict:
    """Actualiza solo los campos enviados en la petición (PATCH)."""
    user = get_user_by_id(user_id)
    update_dict = user_data.model_dump(exclude_unset=True)
    if user:
        for key, value in update_dict.items():
            user[key] = value
    return user

def delete_user(user_id: int) -> bool:
    """Elimina un usuario por ID."""
    user = get_user_by_id(user_id)
    if user:
        db_users.remove(user)
        return True
    return False