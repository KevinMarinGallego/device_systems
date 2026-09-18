from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device


class LoanCreate(BaseModel):

    user_id: int

    device_id: int


class LoanUpdate(BaseModel):

    status: str


class LoanResponse(BaseModel):

    id: int

    user_id: int

    device_id: int

    loan_date: datetime

    return_date: Optional[datetime]

    status: str

    class Config:
        from_attributes = True

class UserBasic(BaseModel):

    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class DeviceBasic(BaseModel):

    id: int
    name: str
    serial_number: str
    device_type: str

    class Config:
        from_attributes = True


class LoanDetailResponse(BaseModel):

    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]

    user: UserBasic

    device: DeviceBasic

    class Config:
        from_attributes = True

    device_id: int

    class Config:
        from_attributes = True
        

def get_loan_details(
    db: Session
):

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
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

def get_loans_by_device(
    db: Session,
    device_id: int
):

    return (
        db.query(Loan)
        .join(Device)
        .where(
            Device.id == device_id
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
        .where(
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
        .where(
            Device.device_type == device_type
        )
        .all()
    )