# app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Depends, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlalchemy.orm import Session
import logging
import shutil
import uuid
from datetime import datetime
from typing import List

from .utils.ai_prediction import preprocess_image, predict_image
from .utils.solution import generate_solution
from .utils.pdf_generator import generate_pdf_with_image
from .schemas import PredictionResponse, Record as RecordSchema
from .database import SessionLocal, engine, Base
from .db_models import Record
from PIL import Image as PILImage

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정 (React 개발 서버 주소 추가)
origins = [
    "http://localhost:3000",  # React 개발 서버 주소
    # 필요한 경우 추가 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 이미지 업로드 경로 설정 (상대 경로 사용)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / 'static' / 'images'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
logger.debug(f"이미지 업로드 디렉토리: {UPLOAD_DIR}")

# PDF 파일 저장 경로 설정
PDF_DIR = BASE_DIR / 'static' / 'pdfs'
PDF_DIR.mkdir(parents=True, exist_ok=True)
logger.debug(f"PDF 파일 저장 디렉토리: {PDF_DIR}")

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory=BASE_DIR / 'static'), name="static")

# 데이터베이스 세션 의존성 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    logger.debug("root endpoint. just only test")
    return {"message": "테스트"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    클라이언트로부터 이미지를 업로드받아 예측을 수행하고 결과를 반환하고, 기록을 저장합니다.
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    try:
        # 고유한 파일 이름 생성 (ASCII 사용)
        unique_filename = f"{uuid.uuid4()}_{file.filename.replace(' ', '_')}"
        file_path = UPLOAD_DIR / unique_filename

        # 파일 저장
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"예측을 위한 이미지 저장: {unique_filename}")

        # 이미지 리사이징 (500x500으로 고정)
        resized_image_filename = f"resized_{unique_filename}"
        resized_image_path = UPLOAD_DIR / resized_image_filename
        with PILImage.open(file_path) as img:
            img = img.convert("RGB")  # 이미지 포맷 통일
            img = img.resize((500, 500))
            img.save(resized_image_path)

        logger.debug(f"이미지 리사이징 완료: {resized_image_path}")

        # 이미지 전처리
        img_array = preprocess_image(str(resized_image_path))

        # 예측 수행
        prediction_result = predict_image(img_array)

        # 이미지 URL 생성 (절대 URL)
        base_url = str(request.base_url).rstrip("/")
        image_url = f"{base_url}/static/images/{resized_image_filename}"

        # 솔루션 생성
        solution = generate_solution(prediction_result["prediction"], prediction_result["score"])

        # PDF 파일명 생성 (ASCII 문자만 사용)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"analysis_{timestamp}.pdf"
        pdf_path = PDF_DIR / pdf_filename

        # PDF 생성
        generate_pdf_with_image(
            output_path=str(pdf_path),
            image_path=str(resized_image_path),  # 로컬 이미지 경로 사용
            prediction=prediction_result["prediction"],
            score=int(prediction_result["score"]),  # 정수로 변환
            solution=solution
        )

        logger.debug(f"PDF 생성 완료: {pdf_path}")

        # PDF 다운로드 URL 생성
        pdf_url = f"{base_url}/download-pdf/{pdf_filename}"

        # 기록 저장
        record = Record(
            name=name,
            prediction=prediction_result["prediction"],
            score=int(prediction_result["score"]),  # 정수로 변환
            pdf_filename=pdf_filename,
            created_at=datetime.utcnow()
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return PredictionResponse(
            prediction=prediction_result["prediction"],
            probabilities=prediction_result["probabilities"],
            score=int(prediction_result["score"]),  # 정수로 변환
            solution=solution,
            image_url=image_url,
            pdf_url=pdf_url  # PDF 다운로드 링크 추가
        )

    except Exception as e:
        logger.error(f"예측 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="예측 중 오류가 발생했습니다.")

@app.get("/download-pdf/{pdf_filename}")
async def download_pdf(pdf_filename: str):
    """
    PDF 파일을 다운로드합니다.
    """
    pdf_path = PDF_DIR / pdf_filename
    if pdf_path.exists():
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename=pdf_filename
        )
    else:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

@app.get("/records", response_model=List[RecordSchema])
def get_records(db: Session = Depends(get_db)):
    """
    모든 분석 기록을 반환합니다.
    """
    records = db.query(Record).order_by(Record.created_at.desc()).all()
    return records
