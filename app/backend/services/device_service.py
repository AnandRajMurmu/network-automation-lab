import os

import psycopg


def get_connection():
    """Create a connection to the device inventory database."""
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=3,
    )


def serialize_device(row: tuple) -> dict:
    """Convert a database row into the existing API response format."""
    return {
        "id": row[0],
        "hostname": row[1],
        "management_ip": str(row[2]),
        "device_type": row[3],
        "location": row[4],
        "status": row[5],
        "created_at": row[6].isoformat(),
    }


def list_devices() -> list[dict]:
    """Retrieve all devices from the inventory."""
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT id, hostname, management_ip, device_type,
                       location, status, created_at
                FROM devices
                ORDER BY id
                """
        )
        rows = cursor.fetchall()

    return [serialize_device(row) for row in rows]


def get_device(device_id: int) -> dict | None:
    """Retrieve one device by its ID."""
    with get_connection() as connection, connection.cursor() as cursor:
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

    return serialize_device(row) if row is not None else None


def create_device(device: dict) -> dict:
    """Insert a device and return the created record."""
    with get_connection() as connection, connection.cursor() as cursor:
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
                device["hostname"],
                str(device["management_ip"]),
                device["device_type"],
                device["location"],
                device["status"],
            ),
        )
        row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Device creation returned no result")

    return serialize_device(row)


def update_device(device_id: int, device: dict) -> dict | None:
    """Update an existing device."""
    with get_connection() as connection, connection.cursor() as cursor:
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
                device["hostname"],
                str(device["management_ip"]),
                device["device_type"],
                device["location"],
                device["status"],
                device_id,
            ),
        )
        row = cursor.fetchone()

    return serialize_device(row) if row is not None else None


def delete_device(device_id: int) -> dict | None:
    """Delete a device and return its ID and hostname."""
    with get_connection() as connection, connection.cursor() as cursor:
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
        return None

    return {
        "id": row[0],
        "hostname": row[1],
    }
