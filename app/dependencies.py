from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from app.OAuth2 import get_current_user
from app import models

formDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
tokenDep = Annotated[str, Depends(oauth_scheme)]

dbDep = Annotated[Session, Depends(get_db)]


def get_active_user(db: dbDep, token: tokenDep):
    return get_current_user(db, token)


activeUser = Annotated[models.User, Depends(get_active_user)]


class PaginationParam:
    def __init__(self, name: str = None, page: int = 1, limit: int = 100):
        self.name = name
        self.page = page
        self.limit = limit


pagination_params = Annotated[PaginationParam, Depends()]
