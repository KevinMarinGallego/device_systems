from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from typing import Literal
from typing import Optional



class UserCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=3
    )

    email: EmailStr

    role: Literal[
        "admin",
        "support",
        "user"
    ]

    is_active: bool


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=3
    )

    email: EmailStr

    role: Literal[
        "admin",
        "support",
        "user"
    ]

    is_active: bool
    
class UserPatch(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None

    role: Optional[
        Literal[
            "admin",
            "support",
            "user"
        ]
    ] = None

    is_active: Optional[bool] = None