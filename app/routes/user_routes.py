"""Rutas de usuarios."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.auth.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.loan_schema import LoanResponse
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services import loan_service, user_service
from app.core.limiter import limiter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Obtiene una lista de usuarios con filtros opcionales.",
    response_description="Lista de usuarios",
    responses={401: {"description": "No autorizado"}},
)
@limiter.limit("30/minute")
def get_users(
    request: Request,
    role: Optional[str] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.get_all_users(db, role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    responses={
        404: {"description": "Usuario no encontrado"},
        401: {"description": "No autorizado"},
    },
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return db_user


@router.get(
    "/{user_id}/loans",
    response_model=List[LoanResponse],
    summary="Obtener préstamos de un usuario",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return loan_service.get_user_loans(db, user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    responses={400: {"description": "Correo ya registrado"}},
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{user.email}' ya está registrado",
        )
    return user_service.create_user(db, user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    responses={
        400: {"description": "Correo ya registrado"},
        404: {"description": "Usuario no encontrado"},
    },
)
def update_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)
):
    if user_data.email:
        other = user_service.get_user_by_email(db, user_data.email)
        if other and other.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo '{user_data.email}' ya está registrado",
            )
    updated_user = user_service.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    responses={
        404: {"description": "Usuario no encontrado"},
        409: {"description": "El usuario tiene préstamos registrados"},
    },
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not user_service.get_user_by_id(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    if loan_service.get_user_loans(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar: el usuario tiene préstamos registrados",
        )
    user_service.delete_user(db, user_id)
    return None