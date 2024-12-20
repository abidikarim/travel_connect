from fastapi import APIRouter, HTTPException, status
from app.services import user
from app.dependencies import dbDep, activeUser, pagination_params
from typing import List
from app import schemas

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: dbDep, curr_user: activeUser, pg_params: pagination_params):
    return user.get_all_users(db, pg_params)


@router.get("/{id}", response_model=schemas.UserOut)
def get_by_id(db: dbDep, id: int, curr_user: activeUser):
    user_db = user.get_user_by_id(db, id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_db


@router.post("/", response_model=schemas.UserOut)
def add_user(db: dbDep, user_data: schemas.UserCreate):
    user_dict = user_data.model_dump()
    return user.create_user(db, user_dict)


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(
    db: dbDep, id: int, user_data: schemas.UserUpdate, curr_user: activeUser
):
    if user_data.new_password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be match"
        )
    user_dict = user_data.model_dump()
    return user.edit_user(db, id, user_dict)


@router.delete("/{id}")
def delete_user(db: dbDep, id: int):
    return user.delete_user(db, id)
