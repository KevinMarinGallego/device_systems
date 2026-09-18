from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailResponse
)

from app.models.user_model import User
from app.models.device_model import Device

from app.services.loan_service import (
    get_loans,
    get_loan_by_id,
    create_loan,
    return_loan,
    get_loan_details,
    get_loans_by_user,
    get_loans_by_status,
    get_loans_by_user_email,
    get_loans_by_device_type
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)
@router.get(
    "",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene todos los préstamos o permite filtrar por estado, correo de usuario o tipo de dispositivo."
)
def list_loans(

    status: str = None,

    user_email: str = None,

    device_type: str = None,

    db: Session = Depends(get_db)
):

    if status:
        return get_loans_by_status(
            db,
            status
        )

    if user_email:
        return get_loans_by_user_email(
            db,
            user_email
        )

    if device_type:
        return get_loans_by_device_type(
            db,
            device_type
        )

    return get_loans(db)

@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Detalle de préstamos",
    description="Muestra la información del préstamo junto con los datos del usuario y del dispositivo."
)

def loan_details(
    db: Session = Depends(get_db)
):

    return get_loan_details(db)


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
    status_code=201,
    summary="Crear préstamo",
    description="Crea un préstamo de un dispositivo.",
    responses={
        404: {
            "description": "Usuario o dispositivo no encontrado"
        },
        409: {
            "description": "Dispositivo no disponible"
        }
    }
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