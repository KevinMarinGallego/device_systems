from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.device_model import Device


def get_devices(
    db: Session
):

    return db.query(Device).all()


def get_device_by_id(
    db: Session,
    device_id: int
):

    return (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )


def get_device_by_serial(
    db: Session,
    serial_number: str
):

    return (
        db.query(Device)
        .filter(
            Device.serial_number == serial_number
        )
        .first()
    )


def create_device(
    db: Session,
    device_data
):

    device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand
    )

    db.add(device)

    db.commit()

    db.refresh(device)

    return device


def update_device(
    db: Session,
    device: Device,
    device_data
):

    device.name = device_data.name
    device.serial_number = (
        device_data.serial_number
    )
    device.device_type = (
        device_data.device_type
    )
    device.brand = device_data.brand
    device.is_available = (
        device_data.is_available
    )

    db.commit()

    db.refresh(device)

    return device


def patch_device(
    db: Session,
    device: Device,
    update_data: dict
):

    for key, value in update_data.items():

        setattr(
            device,
            key,
            value
        )

    db.commit()

    db.refresh(device)

    return device


def delete_device(
    db: Session,
    device: Device
):

    db.delete(device)

    db.commit()


def get_devices_by_type(
    db: Session,
    device_type: str
):

    return (
        db.query(Device)
        .filter(
            Device.device_type == device_type
        )
        .all()
    )


def get_devices_by_availability(
    db: Session,
    is_available: bool
):

    return (
        db.query(Device)
        .filter(
            Device.is_available == is_available
        )
        .all()
    )


def get_devices_by_brand(
    db: Session,
    brand: str
):

    return (
        db.query(Device)
        .filter(
            Device.brand.ilike(f"%{brand}%")
        )
        .all()
    )


def search_devices(
    db: Session,
    search: str
):

    return (
        db.query(Device)
        .filter(
            or_(
                Device.name.ilike(
                    f"%{search}%"
                ),
                Device.brand.ilike(
                    f"%{search}%"
                ),
                Device.serial_number.ilike(
                    f"%{search}%"
                )
            )
        )
        .all()
    )