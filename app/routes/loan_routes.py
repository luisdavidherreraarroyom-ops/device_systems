"""Rutas de préstamos."""
from datetime import date
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.auth.dependencies import get_current_user, require_role
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse
from app.services import loan_service, user_service
from app.core.limiter import limiter

router = APIRouter(prefix="/loans", tags=["Loans"])

LoanStatus = Literal["active", "returned", "overdue"]


def _search_loans(
    db: Session,
    status_filter: Optional[str],
    user_id: Optional[int],
    device_id: Optional[int],
    user_email: Optional[str],
    device_type: Optional[str],
    date_from: Optional[date],
    date_to: Optional[date],
):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="date_from no puede ser posterior a date_to",
        )
    return loan_service.get_all_loans(
        db,
        status_filter=status_filter,
        user_id=user_id,
        device_id=device_id,
        user_email=user_email,
        device_type=device_type,
        date_from=date_from,
        date_to=date_to,
    )


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    summary="Listar préstamos con datos de usuario y dispositivo",
    description="Igual que GET /loans: hace JOIN con users y devices y acepta los mismos filtros.",
    response_description="Lista de préstamos con usuario y dispositivo anidados",
    responses={401: {"description": "No autorizado"}, 403: {"description": "Rol sin permisos"}},
)
def list_loan_details(
    status_filter: Optional[LoanStatus] = Query(None, alias="status"),
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "support")),
):
    return _search_loans(
        db, status_filter, user_id, device_id, user_email, device_type, date_from, date_to
    )


@router.get(
    "",
    response_model=List[LoanDetailResponse],
    summary="Listar préstamos con información detallada y filtros",
    description=(
        "Consulta préstamos con JOIN a usuarios y dispositivos. Filtros opcionales: "
        "status, user_id, device_id, user_email, device_type, date_from y date_to (YYYY-MM-DD)."
    ),
    response_description="Lista de préstamos con usuario y dispositivo anidados",
)
def list_loans(
    status_filter: Optional[LoanStatus] = Query(None, alias="status"),
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
):
    return _search_loans(
        db, status_filter, user_id, device_id, user_email, device_type, date_from, date_to
    )


@router.get(
    "/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Obtener detalle de un préstamo por ID",
    responses={404: {"description": "Préstamo no encontrado"}},
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con ID {loan_id} no encontrado",
        )
    return loan


@router.get(
    "/user/{user_id}",
    response_model=List[LoanDetailResponse],
    summary="Consultar historial de préstamos de un usuario",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    if not user_service.get_user_by_id(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return loan_service.get_user_loans(db, user_id)


@router.get(
    "/device/{device_id}",
    response_model=List[LoanDetailResponse],
    summary="Consultar historial de préstamos de un dispositivo",
)
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    return loan_service.get_device_loans(db, device_id)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo préstamo",
    description="Valida que el usuario y el dispositivo existan y que el dispositivo esté disponible.",
    responses={
        404: {"description": "Usuario o dispositivo no existe"},
        409: {"description": "El dispositivo no está disponible"},
        401: {"description": "No autorizado"},
    },
)
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return loan_service.create_loan(db, loan_data)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver un dispositivo prestado",
    description="Marca el préstamo como 'returned', registra la fecha de devolución y libera el dispositivo.",
    response_description="Préstamo actualizado como devuelto",
    responses={
        404: {"description": "Préstamo no encontrado"},
        409: {"description": "El préstamo ya fue devuelto"},
        401: {"description": "No autorizado"},
        403: {"description": "Rol sin permisos"},
    },
)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "support")),
):
    return loan_service.return_loan(db, loan_id)