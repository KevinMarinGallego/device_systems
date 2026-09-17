from datetime import datetime

from sqlalchemy.orm import Session

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device


def get_loans(
    db: Session
):
    return db.query(Loan).all()


def get_loan_by_id(
    db: Session,
    loan_id: int
):
    return (
        db.query(Loan)
        .filter(Loan.id == loan_id)
        .first()
    )


def create_loan(
    db: Session,
    user: User,
    device: Device
):

    loan = Loan(
        user_id=user.id,
        device_id=device.id,
        status="active"
    )

    device.is_available = False

    db.add(loan)

    db.commit()

    db.refresh(loan)

    return loan


def return_loan(
    db: Session,
    loan: Loan,
    device: Device
):

    loan.status = "returned"

    loan.return_date = datetime.utcnow()

    device.is_available = True

    db.commit()

    db.refresh(loan)

    return loan
