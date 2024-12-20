from sqlalchemy.orm import Session
from app import models
from fastapi import HTTPException, status


def get_error_detail(error: str, error_keys: dict):
    for er in error_keys:
        if er in error:
            return error_keys[er]
    return {"message": "Somthing went wrong", "status": 400}


def add_error(db: Session, error: str, user_id: int = None):
    try:
        new_error = models.Error(error=error, user_id=user_id)
        db.add(new_error)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong"
        )
