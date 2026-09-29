from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=8, description="Contraseña segura")
    role: Literal["admin", "support", "user"] = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contraseña no debe contener espacios en blanco")
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None