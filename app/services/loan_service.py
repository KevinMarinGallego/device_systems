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
def get_loans_by_status(
    db: Session,
    status: str
):

    return (
        db.query(Loan)
        .where(
            Loan.status == status
        )
        .all()
    )
def get_loans_by_user(
    db: Session,
    user_id: int
):

    return (
        db.query(Loan)
        .join(User)
        .where(
            User.id == user_id
        )
        .all()
    )
    
def get_loans_by_user_email(
    db: Session,
    email: str
):
    return (
        db.query(Loan)
        .join(User)
        .filter(
            User.email.ilike(
                f"%{email}%"
            )
        )
        .all()
    )
    
def get_loans_by_device_type(
    db: Session,
    device_type: str
):
    return (
        db.query(Loan)
        .join(Device)
        .filter(
            Device.device_type == device_type
        )
        .all()
    )

def get_loan_details(
    db: Session
):

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .all()
    )
def get_loans_by_device(
    db: Session,
    device_id: int
):
    return (
        db.query(Loan)
        .join(Device)
        .where(Device.id == device_id)
        .all()
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
