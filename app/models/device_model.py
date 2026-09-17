from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Device(Base):

    __tablename__ = "devices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    serial_number = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    device_type = Column(
        String,
        nullable=False
    )

    brand = Column(
        String,
        nullable=True
    )

    is_available = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    loans = relationship(
        "Loan",
        back_populates="device"
    )