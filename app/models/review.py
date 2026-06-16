from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from app.database.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    language = Column(String(50))
    code = Column(Text)

    quality_score = Column(Integer, nullable=True)
    security_score = Column(Integer, nullable=True)
    performance_score = Column(Integer, nullable=True)

    issues = Column(Text, nullable=True)
    suggestions = Column(Text, nullable=True)
    improved_code = Column(Text, nullable=True)

    status = Column(String(20), default="PENDING")

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))