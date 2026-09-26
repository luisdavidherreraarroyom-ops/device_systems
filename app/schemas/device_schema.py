from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Esquema base con atributos comunes
class DeviceBase(BaseModel):
    name: str = Field(..., example="Laptop Lenovo ThinkPad")
    serial_number: str = Field(..., example="LEN-2024-001")
    device_type: str = Field(..., example="laptop")
    brand: Optional[str] = Field(None, example="Lenovo")


# Esquema para la creación de un dispositivo
class DeviceCreate(DeviceBase):
    pass


# Esquema para la actualización de un dispositivo (todos los campos opcionales)
class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Laptop Lenovo ThinkPad T14")
    serial_number: Optional[str] = Field(None, example="LEN-2024-002")
    device_type: Optional[str] = Field(None, example="laptop")
    brand: Optional[str] = Field(None, example="Lenovo")
    is_available: Optional[bool] = Field(None, example=True)


# Esquema para la respuesta HTTP
class DeviceResponse(DeviceBase):
    id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True