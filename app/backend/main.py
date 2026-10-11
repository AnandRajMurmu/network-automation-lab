import os
from typing import Literal

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress

app = FastAPI(
    title="Network Automation Lab API",
    description="Backend API for the network automation platform",
    version="0.1.0",
    root_path="/api",
)


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


@app.get("/")
def root():
    return {"message": "Network Automation Lab API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-health")
def database_health():
    try:
        with (
            psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3,
            ) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return {"database": "connected"}

    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Database Connection Unavailable.",
        )


@app.get("/devices")
def list_devices():
    try:
        with (
            psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3,
        ) as connection,
            connection.cursor() as cursor,
        ):
                cursor.execute(
                    """
                    SELECT id, hostname, management_ip, device_type,
                           location, status, created_at
                    FROM devices
                    ORDER BY id
                    """
                )
                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "hostname": row[1],
                "management_ip": str(row[2]),
                "device_type": row[3],
                "location": row[4],
                "status": row[5],
                "created_at": row[6].isoformat(),
            }
            for row in rows
        ]

    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve device inventory",
        ) from None

@app.post("/devices", status_code=201)
def create_device(device: DeviceCreate):
    try:
        with (
            psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3,
            ) as connection,
                connection.cursor() as cursor,
            ):
                cursor.execute(
                    """
                    INSERT INTO devices (
                        hostname,
                        management_ip,
                        device_type,
                        location,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, hostname, management_ip,
                              device_type, location, status, created_at
                    """,
                    (
                        device.hostname,
                        str(device.management_ip),
                        device.device_type,
                        device.location,
                        device.status,
                    ),
                )
                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(
                        status_code=500,
                        detail="Device creation returned no result",
                    )

        return {
            "id": row[0],
            "hostname": row[1],
            "management_ip": str(row[2]),
            "device_type": row[3],
            "location": row[4],
            "status": row[5],
            "created_at": row[6].isoformat(),
        }

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


@app.get("/devices/{device_id}")
def get_device(device_id: int):
    try:
        with (
            psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3,
            ) as connection,
                 connection.cursor() as cursor,
            ):
                cursor.execute(
                    """
                    SELECT id, hostname, management_ip, device_type,
                           location, status, created_at
                    FROM devices
                    WHERE id = %s
                    """,
                    (device_id,),
                )
                row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Device not found",
            )

        return {
            "id": row[0],
            "hostname": row[1],
            "management_ip": str(row[2]),
            "device_type": row[3],
            "location": row[4],
            "status": row[5],
            "created_at": row[6].isoformat(),
        }

    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve device",
        ) from None


@app.put("/devices/{device_id}")
def update_device(device_id: int, device: DeviceCreate):
    try:
        with(
            psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3,
            ) as connection,
                connection.cursor() as cursor,
            ):
                cursor.execute(
                    """
                    UPDATE devices
                    SET hostname = %s,
                        management_ip = %s,
                        device_type = %s,
                        location = %s,
                        status = %s
                    WHERE id = %s
                    RETURNING id, hostname, management_ip,
                              device_type, location, status, created_at
                    """,
                    (
                        device.hostname,
                        str(device.management_ip),
                        device.device_type,
                        device.location,
                        device.status,
                        device_id,
                    ),
                )
                row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Device not found",
            )

        return {
            "id": row[0],
            "hostname": row[1],
            "management_ip": str(row[2]),
            "device_type": row[3],
            "location": row[4],
            "status": row[5],
            "created_at": row[6].isoformat(),
        }

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


@app.delete("/devices/{device_id}")
def delete_device(device_id: int):
    try:
        with(
            psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3,
            ) as connection,
                connection.cursor() as cursor,
            ):
                cursor.execute(
                    """
                    DELETE FROM devices
                    WHERE id = %s
                    RETURNING id, hostname
                    """,
                    (device_id,),
                )
                row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Device not found",
            )

        return {
            "message": "Device deleted successfully",
            "id": row[0],
            "hostname": row[1],
        }

    except (psycopg.Error, KeyError):
        raise HTTPException(
            status_code=503,
            detail="Unable to delete device",
        ) from None
