from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Modelo base con los atributos comunes de un usuario
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["johndoe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    role: str = Field(default="operator", examples=["admin"])
    is_active: bool = Field(default=True)

# Modelo para la creación de usuarios (requiere contraseña)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, examples=["secret123"])

# Modelo para la actualización parcial de usuarios (todos los campos opcionales)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

# Modelo para la respuesta de la API (no expone la contraseña e incluye el ID asignado)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True