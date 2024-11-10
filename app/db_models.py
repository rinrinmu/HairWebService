# app/db_models.py

from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    pdf_filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
