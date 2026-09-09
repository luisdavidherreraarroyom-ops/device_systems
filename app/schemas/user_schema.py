from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

# Roles permitidos en la aplicación
ALLOWED_ROLES = Literal["admin", "developer", "support", "user"]

# Base común para esquemas
class UserBase(BaseModel):
    name: str = Field(..., example="Luis Herrera")
    email: EmailStr = Field(..., example="luis@example.com")
    role: ALLOWED_ROLES = Field(..., example="developer")
    is_active: bool = Field(default=True, example=True)

# Esquema para crear (POST) o actualizar completo (PUT)
class UserCreate(UserBase):
    pass

# Esquema para actualización parcial (PATCH) - Todos los campos opcionales
class UserUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, example="Luis Herrera Modificado")
    email: Optional[EmailStr] = Field(None, example="luis_nuevo@example.com")
    role: Optional[ALLOWED_ROLES] = Field(None, example="admin")
    is_active: Optional[bool] = Field(None, example=False)

# Esquema para respuestas de la API
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True