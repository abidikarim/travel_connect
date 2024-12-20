from passlib.context import CryptContext
from app.config import settings
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from app import schemas
from fastapi import status, HTTPException
from app import models

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_pwd: str, hashed_pwd: str):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def create_access_token(payload_data: dict):
    to_encode = payload_data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = payload.get("user_id")
        return schemas.PayloadData(user_id=id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired"
        )
    except PyJWTError:
        raise credentials_exception


def get_current_user(db, token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == payload_data.user_id).first()
    return user
