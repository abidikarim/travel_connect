from app.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey


class Error(Base):
    __tablename__ = "errors"
    id = Column(Integer, primary_key=True)
    error = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_on = Column(TIMESTAMP(timezone=True))
