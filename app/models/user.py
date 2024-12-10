from app.database import Base
from app.enums import Gender, AccountStatus
from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    Enum,
    func,
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone_number = Column(String, nullable=True)
    status = Column(Enum(AccountStatus), server_default=AccountStatus.Active.value)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
