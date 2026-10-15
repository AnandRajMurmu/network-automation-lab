import os

import psycopg
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Network Automation Lab API"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/db-health")
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

    except (psycopg.Error, KeyError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Database Connection Unavailable.",
        ) from exc
