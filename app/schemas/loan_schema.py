from datetime import datetime

from pydantic import BaseModel

from typing import Optional


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


class LoanDetailResponse(BaseModel):

    id: int

    status: str

    loan_date: datetime

    return_date: Optional[datetime]

    user_id: int

    device_id: int

    class Config:
        from_attributes = True
        
        