from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"]
)

http_basic = HTTPBasic()

@router.get("/basic_auth/")
async def basic_credentials_auth(credentials: Annotated[HTTPBasicCredentials, Depends(http_basic)]):
    return {
        "message": "Barya",
        "username": credentials.username,
        "password": credentials.password
    }
