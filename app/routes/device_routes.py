from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DevicePatch,
    DeviceResponse
)

from app.services.device_service import (
    get_devices,
    get_device_by_id,
    get_device_by_serial,
    create_device,
    update_device,
    patch_device,
    delete_device,
    get_devices_by_type,
    get_devices_by_availability,
    get_devices_by_brand,
    search_devices
)
from app.services.loan_service import (
    get_loans_by_device
)
from app.dependencies.auth_dependency import (
    require_admin
)
router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get("", response_model=list[DeviceResponse])
def list_devices(
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):

    if device_type:
        return get_devices_by_type(db, device_type)

    if is_available is not None:
        return get_devices_by_availability(
            db,
            is_available
        )

    if brand:
        return get_devices_by_brand(
            db,
            brand
        )

    if search:
        return search_devices(
            db,
            search
        )

    return get_devices(db)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db)
):

    device = get_device_by_id(
        db,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return device


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=201
)
def create_new_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    existing_device = get_device_by_serial(
        db,
        device_data.serial_number
    )

    if existing_device:
        raise HTTPException(
            status_code=400,
            detail="Número de serie duplicado"
        )

    return create_device(
        db,
        device_data
    )


@router.put(
    "/{device_id}",
    response_model=DeviceResponse
)
def update_existing_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):

    device = get_device_by_id(
        db,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return update_device(
        db,
        device,
        device_data
    )


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse
)
def patch_existing_device(
    device_id: int,
    device_data: DevicePatch,
    db: Session = Depends(get_db)
):

    update_data = device_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron campos para actualizar"
        )

    device = get_device_by_id(
        db,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return patch_device(
        db,
        device,
        update_data
    )


@router.delete("/{device_id}")
def remove_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    device = get_device_by_id(
        db,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    delete_device(
        db,
        device
    )

    return {
        "detail": "Dispositivo eliminado correctamente"
    }
    
@router.get(
    "/{device_id}/loans"
)
def device_loans(
    device_id: int,
    db: Session = Depends(get_db)
):

    return get_loans_by_device(
        db,
        device_id
    )