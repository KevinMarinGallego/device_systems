from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse
)

from app.models.user_model import User
from app.models.device_model import Device

from app.services.loan_service import (
    get_loans,
    get_loan_by_id,
    create_loan,
    return_loan
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)
@router.get(
    "",
    response_model=list[LoanResponse]
)
def list_loans(
    db: Session = Depends(get_db)
):

    return get_loans(db)

@router.get(
    "/{loan_id}",
    response_model=LoanResponse
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    loan = get_loan_by_id(
        db,
        loan_id
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Prestamo no encontrado"
        )

    return loan

@router.post(
    "",
    response_model=LoanResponse,
    status_code=201
)
def create_new_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == loan_data.user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    device = (
        db.query(Device)
        .filter(
            Device.id == loan_data.device_id
        )
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail="Dispositivo no disponible"
        )

    return create_loan(
        db,
        user,
        device
    )
    
@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse
)
def return_device(
    loan_id: int,
    db: Session = Depends(get_db)
):

    loan = get_loan_by_id(
        db,
        loan_id
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Prestamo no encontrado"
        )

    if loan.status == "returned":
        raise HTTPException(
            status_code=409,
            detail="Prestamo ya devuelto"
        )

    device = (
        db.query(Device)
        .filter(
            Device.id == loan.device_id
        )
        .first()
    )

    return return_loan(
        db,
        loan,
        device
    )

