"""Servicio de dispositivos: consultas y operaciones sobre la tabla devices."""
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def get_all_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Device]:
    """Lista dispositivos con filtros opcionales."""
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type.ilike(device_type))
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
            )
        )
    return query.order_by(Device.id).all()


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    """Devuelve el dispositivo o None si no existe."""
    return db.query(Device).filter(Device.id == device_id).first()


def get_device_by_serial(db: Session, serial_number: str) -> Optional[Device]:
    """Busca un dispositivo por número de serie."""
    return db.query(Device).filter(Device.serial_number == serial_number).first()


def create_device(db: Session, device_data: DeviceCreate) -> Device:
    """Crea un dispositivo."""
    new_device = Device(**device_data.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


def update_device(
    db: Session, device_id: int, device_data: DeviceUpdate
) -> Optional[Device]:
    """Actualiza (PUT o PATCH) solo los campos enviados. None si no existe."""
    device = get_device_by_id(db, device_id)
    if not device:
        return None

    changes = device_data.model_dump(exclude_unset=True)

    new_serial = changes.get("serial_number")
    if new_serial and new_serial != device.serial_number:
        if get_device_by_serial(db, new_serial):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de serie ya está en uso por otro dispositivo",
            )

    for key, value in changes.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> bool:
    """Elimina el dispositivo. False si no existe."""
    device = get_device_by_id(db, device_id)
    if not device:
        return False
    db.delete(device)
    db.commit()
    return True