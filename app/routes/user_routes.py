from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    order_by: Optional[str] = Query("id", description="Ordenar por: id, name, created_at"),
    db: Session = Depends(get_db),
):
    return UserService.get_all(db, role=role, is_active=is_active, order_by=order_by)

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_by_id(db, user_id)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserService.create(db, user_data)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update(db, user_id, user_data)

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(user_id: int, user_data: UserPatch, db: Session = Depends(get_db)):
    return UserService.patch(db, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService.delete(db, user_id)
    return {"detail": f"Usuario con ID {user_id} eliminado exitosamente"}