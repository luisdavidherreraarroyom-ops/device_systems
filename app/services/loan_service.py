"""Servicio de préstamos: consultas con joins y reglas de negocio."""
from datetime import date, datetime, time, timezone
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate


def get_all_loans(
    db: Session,
    status_filter: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[Loan]:
    """Consulta préstamos con JOIN a User y Device y filtros opcionales."""
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    conditions = []
    if status_filter:
        conditions.append(Loan.status == status_filter)
    if user_id is not None:
        conditions.append(Loan.user_id == user_id)
    if device_id is not None:
        conditions.append(Loan.device_id == device_id)
    if user_email:
        conditions.append(User.email.ilike(f"%{user_email}%"))
    if device_type:
        conditions.append(Device.device_type.ilike(f"%{device_type}%"))
    if date_from:
        conditions.append(Loan.loan_date >= datetime.combine(date_from, time.min))
    if date_to:
        conditions.append(Loan.loan_date <= datetime.combine(date_to, time.max))

    if conditions:
        query = query.filter(and_(*conditions))

    return query.order_by(Loan.id).all()


def get_loan_by_id(db: Session, loan_id: int) -> Optional[Loan]:
    return db.query(Loan).filter(Loan.id == loan_id).first()


def get_user_loans(db: Session, user_id: int) -> List[Loan]:
    return db.query(Loan).filter(Loan.user_id == user_id).order_by(Loan.id).all()


def get_device_loans(db: Session, device_id: int) -> List[Loan]:
    return db.query(Loan).filter(Loan.device_id == device_id).order_by(Loan.id).all()


def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con ID {loan_data.user_id} no existe",
        )

    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El dispositivo con ID {loan_data.device_id} no existe",
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El dispositivo '{device.name}' (ID {device.id}) no está disponible",
        )

    new_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active",
        loan_date=datetime.now(timezone.utc),
    )
    device.is_available = False

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan


def return_loan(db: Session, loan_id: int) -> Loan:
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El préstamo con ID {loan_id} no existe",
        )

    if loan.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El préstamo con ID {loan_id} ya fue devuelto",
        )

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan