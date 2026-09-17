from pydantic import BaseModel
from pydantic import Field

from typing import Optional
from typing import Literal


class DeviceCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=3
    )

    serial_number: str

    device_type: Literal[
        "laptop",
        "tablet",
        "proyector",
        "camara",
        "router",
        "monitor"
    ]

    brand: Optional[str] = None


class DeviceUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=3
    )

    serial_number: str

    device_type: Literal[
        "laptop",
        "tablet",
        "proyector",
        "camara",
        "router",
        "monitor"
    ]

    brand: Optional[str] = None

    is_available: bool


class DevicePatch(BaseModel):

    name: Optional[str] = None

    serial_number: Optional[str] = None

    device_type: Optional[str] = None

    brand: Optional[str] = None

    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):

    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True