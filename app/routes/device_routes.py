"""Rutas de dispositivos."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services import device_service, loan_service

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get(
    "",
    response_model=List[DeviceResponse],
    summary="Listar dispositivos con filtros",
    description=(
        "Obtiene todos los dispositivos tecnológicos registrados con opción de "
        "filtrar por tipo, disponibilidad, marca o término de búsqueda."
    ),
    response_description="Lista de dispositivos",
)
def list_devices(
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return device_service.get_all_devices(
        db,
        device_type=device_type,
        is_available=is_available,
        brand=brand,
        search=search,
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener un dispositivo por ID",
    responses={404: {"description": "Dispositivo no encontrado"}},
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {device_id} no encontrado",
        )
    return device


@router.get(
    "/{device_id}/loans",
    response_model=List[LoanDetailResponse],
    summary="Historial de préstamos de un dispositivo",
    responses={404: {"description": "Dispositivo no encontrado"}},
)
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    if not device_service.get_device_by_id(db, device_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {device_id} no encontrado",
        )
    return loan_service.get_device_loans(db, device_id)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo dispositivo",
    responses={400: {"description": "Número de serie duplicado"}},
)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    existing_device = device_service.get_device_by_serial(db, device.serial_number)
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Ya existe un dispositivo registrado con el número de serie "
                f"'{device.serial_number}'"
            ),
        )
    return device_service.create_device(db, device)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar un dispositivo completamente",
    responses={
        400: {"description": "Número de serie duplicado"},
        404: {"description": "Dispositivo no encontrado"},
    },
)
def update_device(
    device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)
):
    updated_device = device_service.update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {device_id} no encontrado",
        )
    return updated_device


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar un dispositivo parcialmente",
    responses={
        400: {"description": "Número de serie duplicado"},
        404: {"description": "Dispositivo no encontrado"},
    },
)
def patch_device(
    device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)
):
    updated_device = device_service.update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {device_id} no encontrado",
        )
    return updated_device


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un dispositivo",
    responses={
        404: {"description": "Dispositivo no encontrado"},
        409: {"description": "El dispositivo tiene préstamos registrados"},
    },
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    if not device_service.get_device_by_id(db, device_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {device_id} no encontrado",
        )
    if loan_service.get_device_loans(db, device_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar: el dispositivo tiene préstamos registrados",
        )
    device_service.delete_device(db, device_id)
    return None