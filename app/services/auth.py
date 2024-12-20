from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models
import uuid
from app.utilities import send_mail
from app import schemas
from fastapi.responses import JSONResponse
from datetime import datetime
from app.enums import CodeStatus
from app.OAuth2 import get_password_hash, verify_password, create_access_token
from app.services.error import add_error
from app.services import user


def get_code(db: Session, code: str):
    try:
        code_db = (
            db.query(models.ResetPassword)
            .filter(models.ResetPassword.code == code)
            .first()
        )
        if not code_db:
            return None
        return code_db
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def verify_code(code: models.ResetPassword):
    if (datetime.now() - code.created_on.replace(tzinfo=None)).days > 1:
        return False
    return True


async def forget_password(db: Session, email: str):
    try:
        user_db = user.get_user_by_email(db, email)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        new_code = models.ResetPassword(
            email=user_db.email, user_id=user_db.id, code=uuid.uuid4()
        )
        db.add(new_code)
        await send_mail(
            schemas.MailData(
                emails=[user_db.email],
                body={
                    "name": f"{user_db.first_name } {user_db.last_name}",
                    "code": new_code.code,
                },
                subject="Reset Password",
                template="reset_password.html",
            )
        )
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "A password reset link has been sent, check your email"
            },
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        db.rollback()
        add_error(db, str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def reset_password(db: Session, reset_pwd_data: dict):
    try:
        code_db = get_code(db, reset_pwd_data["code"])
        if not code_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Code not found"
            )
        if not verify_code(code_db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code expired"
            )
        if code_db.status == CodeStatus.Used.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code already used"
            )
        db.query(models.User).filter(models.User.id == code_db.user_id).update(
            {"password": get_password_hash(reset_pwd_data["password"])}
        )
        db.query(models.ResetPassword).filter(
            models.ResetPassword.id == code_db.id
        ).update({"status": CodeStatus.Used.value})
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Password has been reset successfully"},
        )
    except Exception as error:
        db.rollback()
        add_error(db, str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def login(db: Session, user_credentials: dict):
    try:
        user_db = user.get_user_by_email(db, user_credentials["email"])
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not verify_password(user_credentials["password"], user_db.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password"
            )
        encoded_jwt = create_access_token(payload_data={"user_id": user_db.id})
        return schemas.AccessToken(token=encoded_jwt, token_type="Bearer")
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
