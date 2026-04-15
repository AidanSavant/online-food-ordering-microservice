import os
import jwt

from uuid import UUID
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from errors.exceptions import UnauthorizedException, InternalServerException

security: HTTPBearer = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "HS256"
JWT_EXPIRY_MIN = 60

def create_access_token(customer_id: UUID, username: str) -> str:
    payload = {
        "sub" : str(customer_id),
        "username": username,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(minutes=JWT_EXPIRY_MIN)
    }

    if not JWT_SECRET:
        raise InternalServerException("Failed to create access token! Reason: JWT_SECRET is not set in environment variables!")

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_access_token(token: str) -> dict:
    if not JWT_SECRET:
        raise InternalServerException("Failed to decode access token! Reason: JWT_SECRET is not set in environment variables!")

    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Access token has expired!")
    
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid access token!")

def decode_customer_id(token: str) -> UUID:
    token_payload = decode_access_token(token)
    decoded_customer_id = token_payload.get("sub")
    if not decoded_customer_id:
        raise UnauthorizedException("Invalid access token! Reason: 'sub' claim is missing!")

    return UUID(decoded_customer_id)

async def get_curr_customer_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    token = credentials.credentials
    return decode_customer_id(token)
