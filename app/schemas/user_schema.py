from pydantic import BaseModel, EmailStr, Field
from typing import Literal

# Restricción de roles
UserRole = Literal["admin", "support", "user"]

# Campos base
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, examples=["Luis Herrera"])
    email: EmailStr = Field(..., examples=["luis@device.com"])
    role: UserRole = Field(default="user", examples=["admin"])
    is_active: bool = Field(default=True, examples=[True])

# Modelo para creación (entrada)
class UserCreate(UserBase):
    pass

# Modelo de respuesta para la API (salida)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True