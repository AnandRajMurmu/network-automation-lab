from typing import Literal

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress
from services import device_service

router = APIRouter()


class DeviceCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    hostname: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$",
    )
    management_ip: IPvAnyAddress
    device_type: str = Field(min_length=1, max_length=50)
    location: str = Field(min_length=1, max_length=100)
    status: Literal["active", "inactive", "maintenance"] = "active"


@router.get("/devices")
def list_devices():
    try:
        return device_service.list_devices()
    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve device inventory",
        ) from None


@router.post("/devices", status_code=201)
def create_device(device: DeviceCreate):
    try:
        return device_service.create_device(device.model_dump())
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Hostname or management IP already exists",
        ) from None
    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to create device",
        ) from None
    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get("/devices/{device_id}")
def get_device(device_id: int):
    try:
        device = device_service.get_device(device_id)
    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve device",
        ) from None

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device


@router.put("/devices/{device_id}")
def update_device(device_id: int, device: DeviceCreate):
    try:
        updated_device = device_service.update_device(
            device_id,
            device.model_dump(),
        )
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Hostname or management IP already exists",
        ) from None
    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to update device",
        ) from None

    if updated_device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return updated_device


@router.delete("/devices/{device_id}")
def delete_device(device_id: int):
    try:
        deleted_device = device_service.delete_device(device_id)
    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to delete device",
        ) from None

    if deleted_device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return {
        "message": "Device deleted successfully",
        **deleted_device,
    }
