from pydantic import BaseModel, EmailStr
from app.enums import Gender, AccountStatus

from datetime import datetime

from typing import List, Dict, Any


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True


class UserBase(OurBaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    gender: Gender
    phone_number: str | None = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    status: AccountStatus
    created_on: datetime


class UserUpdate(OurBaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: Gender | None = None
    phone_number: str | None = None
    new_password: str | None = None
    confirm_password: str | None = None
    actual_password: str


class MailData(OurBaseModel):
    emails: List[EmailStr]
    body: Dict[str, Any]
    template: str
    subject: str


class ResetPassword(OurBaseModel):
    password: str
    confirm_password: str


class AccessToken(OurBaseModel):
    token: str
    token_type: str


class PayloadData(OurBaseModel):
    user_id: int
