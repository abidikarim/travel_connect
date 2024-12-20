from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from fastapi import HTTPException, status
from app.OAuth2 import get_password_hash, verify_password
from app.services.error import get_error_detail, add_error
from fastapi.responses import JSONResponse
from app.dependencies import pagination_params

error_keys = {"users_email_key": {"message": "Email already used", "status": 409}}


def get_all_users(db: Session, pg_params: pagination_params):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.User)
    try:
        if pg_params.name != None:
            query = query.filter(
                func.lower(
                    func.concat(models.User.last_name, " ", models.User.first_name)
                ).contains(func.lower(pg_params.name))
            )
        users = query.limit(pg_params.limit).offset(skip).all()
        return users
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def get_user_by_id(db: Session, id: int):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            return None
        return user
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def get_user_by_email(db: Session, email: str):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            return None
        return user
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def create_user(db: Session, user: dict):
    try:
        user["password"] = get_password_hash(user["password"])
        new_user = models.User(**user)
        db.add(new_user)
        db.commit()
        return new_user
    except Exception as error:
        db.rollback()
        add_error(db=db, error=str(error))
        error_detail = get_error_detail(str(error), error_keys)
        raise HTTPException(
            status_code=error_detail["status"], detail=error_detail["message"]
        )


def edit_user(db: Session, id: int, user_data: dict):
    try:
        user_db = get_user_by_id(db, id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not verify_password(user_data["actual_password"], user_db.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password"
            )
        user_data.pop("actual_password", None)
        user_data = {k: v for k, v in user_data.items() if v is not None}
        if "new_password" in user_data:
            user_data["password"] = get_password_hash(user_data["new_password"])
            for key in ["new_password", "confirm_password"]:
                user_data.pop(key, None)
        db.query(models.User).filter(models.User.id == id).update(user_data)
        db.commit()
        return user_db
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        db.rollback()
        add_error(db=db, error=str(error), user_id=user_db.id)
        error_detail = get_error_detail(str(error), error_keys)
        raise HTTPException(
            status_code=error_detail["status"], detail=error_detail["message"]
        )


def delete_user(db: Session, id: int):
    try:
        user_db = get_user_by_id(db, id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        db.query(models.User).filter(models.User.id == id).delete()
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "User has been deleted"}
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
