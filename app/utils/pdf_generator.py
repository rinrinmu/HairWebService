# app/utils/pdf_generator.py

import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from datetime import datetime
from PIL import Image as PILImage

# 로깅 설정
logger = logging.getLogger(__name__)

def generate_pdf_with_image(output_path: str, image_path: str, prediction: str, score: int, solution: str) -> None:
    """
    한글 텍스트와 이미지를 포함하는 PDF를 생성합니다.

    Parameters:
    - output_path (str): 생성할 PDF 파일의 경로
    - image_path (str): 삽입할 이미지 파일의 로컬 경로
    - prediction (str): 판정 결과
    - score (int): 두피 점수
    - solution (str): 솔루션 텍스트
    """
    try:
        # 한글 폰트 등록
        BASE_DIR = Path(__file__).resolve().parent.parent  # 'app/utils'에서 'app'으로 이동
        FONT_DIR = BASE_DIR / 'static' / 'fonts'
        font_regular = FONT_DIR / 'malgun.ttf'
        font_bold = FONT_DIR / 'malgunbd.ttf'

        logger.debug(f"폰트 경로 (일반): {font_regular}")
        logger.debug(f"폰트 경로 (볼드): {font_bold}")
        logger.debug(f"폰트 존재 여부: {font_regular.exists()}, {font_bold.exists()}")

        if not font_regular.exists() or not font_bold.exists():
            logger.error(f"폰트 파일을 찾을 수 없습니다: {font_regular} 또는 {font_bold}")
            raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_regular} 또는 {font_bold}")

        # 폰트 등록
        pdfmetrics.registerFont(TTFont('MalgunGothic', str(font_regular)))
        pdfmetrics.registerFont(TTFont('MalgunGothic-Bold', str(font_bold)))
        pdfmetrics.registerFontFamily('MalgunGothic',
                                      normal='MalgunGothic',
                                      bold='MalgunGothic-Bold')
        logger.debug("폰트 등록 성공")

        # 스타일 정의
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='Title',
            fontName='MalgunGothic-Bold',
            fontSize=24,
            alignment=1,  # 중앙 정렬
            spaceAfter=12
        )

        small_style = ParagraphStyle(
            name='Small',
            fontName='MalgunGothic',
            fontSize=10,
            leading=12,
            alignment=1,  # 중앙 정렬
            spaceAfter=12
        )

        normal_style = ParagraphStyle(
            name='Normal',
            fontName='MalgunGothic',
            fontSize=12,
            leading=15,
            spaceAfter=12
        )

        # PDF 문서 생성
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        elements = []

        # 제목 추가
        title = Paragraph("두피 분석 간단 보고서", title_style)
        elements.append(title)

        # 분석 완료 시간 추가
        analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_text = f"분석 완료 시간: {analysis_time}"
        elements.append(Paragraph(time_text, small_style))

        # 제목과 본문을 나누는 선 추가
        hr = HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey)
        elements.append(hr)
        elements.append(Spacer(1, 12))

        # 이미지 삽입
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

            # PIL을 사용하여 이미지 크기 조절 (원본을 변경하지 않음)
            with PILImage.open(image_path) as img:
                img = img.convert('RGB')  # RGB 모드로 변환
                img_width, img_height = img.size
                aspect = img_height / float(img_width)
                img_display_width = 4 * inch
                img_display_height = img_display_width * aspect

            rl_image = RLImage(image_path, width=img_display_width, height=img_display_height)
            elements.append(rl_image)
            logger.debug(f"이미지 삽입 성공: {image_path}")
        except Exception as e:
            error_paragraph = Paragraph(f"이미지 삽입 실패: {e}", normal_style)
            elements.append(error_paragraph)
            logger.error(f"이미지 삽입 중 오류 발생: {e}")

        elements.append(Spacer(1, 12))

        # 판정 결과 및 두피 점수 (Bold 사용)
        prediction_text = f"<b>판정 결과:</b> {prediction}"
        score_text = f"<b>두피 점수:</b> {score}점"  # score는 정수로 전달됨
        elements.append(Paragraph(prediction_text, normal_style))
        elements.append(Paragraph(score_text, normal_style))
        elements.append(Spacer(1, 12))

        # 솔루션
        solution_text = f"<b>솔루션:</b> {solution.replace('\n', '<br />')}"
        elements.append(Paragraph(solution_text, normal_style))
        elements.append(Spacer(1, 12))

        # PDF 생성
        try:
            doc.build(elements)
            logger.info(f"PDF 파일 생성 완료: {output_path}")
        except Exception as e:
            logger.error(f"PDF 빌드 중 오류 발생: {e}")
            raise e

    except Exception as main_exception:
        logger.error(f"PDF 생성 중 오류 발생: {main_exception}")
        raise main_exception
