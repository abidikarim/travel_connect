from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db

dbDep = Annotated[Session, Depends(get_db)]
