from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdatePartial
from app.services import user_service
from app.dependencies.user_dependencies import get_user_or_404, validate_unique_email, verify_custom_header

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_custom_header)]
)

@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna la lista general de usuarios con filtros opcionales por rol o estado.",
    response_description="Lista de usuarios encontrada"
)
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, developer, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo (true/false)")
):
    return user_service.get_all_users(role=role, is_active=is_active)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Retorna la información detallada de un usuario específico por su ID.",
    response_description="Usuario encontrado"
)
def get_user(user: dict = Depends(get_user_or_404)):
    return user

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Crea un nuevo usuario validando que el correo no esté duplicado.",
    response_description="Usuario creado exitosamente"
)
def create_user(user_data: UserCreate):
    validate_unique_email(user_data.email)
    return user_service.create_user(user_data)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completamente",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado correctamente"
)
def update_user_put(
    user_data: UserCreate,
    user: dict = Depends(get_user_or_404)
):
    validate_unique_email(user_data.email, current_user_id=user["id"])
    return user_service.update_user_full(user["id"], user_data)

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Modifica únicamente uno o varios campos enviados por el cliente.",
    response_description="Usuario modificado parcialmente"
)
def update_user_patch(
    user_data: UserUpdatePartial,
    user: dict = Depends(get_user_or_404)
):
    update_fields = user_data.model_dump(exclude_unset=True)
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    
    if "email" in update_fields:
        validate_unique_email(update_fields["email"], current_user_id=user["id"])

    return user_service.update_user_partial(user["id"], user_data)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina un usuario existente del sistema por su ID.",
    response_description="Mensaje de confirmación de eliminación"
)
def delete_user(user: dict = Depends(get_user_or_404)):
    user_service.delete_user(user["id"])
    return {"message": f"Usuario con ID {user['id']} eliminado correctamente"}