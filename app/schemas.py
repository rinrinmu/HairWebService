# app/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import List

class PredictionResponse(BaseModel):
    prediction: str
    probabilities: List[float]
    score: int
    solution: str
    image_url: str
    pdf_url: str  # PDF 다운로드 링크 추가

class RecordBase(BaseModel):
    name: str
    prediction: str
    score: int
    pdf_filename: str
    created_at: datetime

class RecordCreate(RecordBase):
    pass

class Record(RecordBase):
    id: int

    class Config:
        from_attributes = True  # orm_mode를 from_attributes로 변경
