from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func, Enum
from app.enums import CodeStatus


class ResetPassword(Base):
    __tablename__ = "reset_passwords"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    code = Column(String, nullable=False)
    status = Column(Enum(CodeStatus), server_default=CodeStatus.Pending.value)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
