from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    contact = Column(String(20))
    security_question = Column(String(255))
    security_answer = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"))