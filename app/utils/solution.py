# app/utils/solution.py

import openai
import os
import logging
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_solution(prediction: str, score: float) -> str:
    """
    예측 결과와 점수를 기반으로 솔루션을 생성합니다.

    Parameters:
    - prediction (str): 예측된 클래스 ("양호", "경증", "중증")
    - score (float): 계산된 점수

    Returns:
    - str: 생성된 솔루션 텍스트
    """
    prompt = (
        f"당신은 두피 건강 전문가입니다. 분석 결과 두피 상태는 '{prediction}'이며, 점수는 {score}점입니다. "
        "이 상태에 대한 효과적인 솔루션을 공백 포함 400자 이내로 제시해주세요. 각 점수대 별 첫 문장이 있으면 좋을 것 같아요."
    )

    try:
        # 클라이언트 인스턴스 생성
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")  # 명시적으로 API 키 전달
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",  # 정확한 모델명 기입
            messages=[
                {"role": "system", "content": "당신은 두피 건강 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # 응답 길이 제한
            temperature=0.6  # 창의성 조절
        )
        # 응답 객체의 속성에 접근 (['content'] 대신 .content 사용)
        solution = response.choices[0].message.content.strip()
        logger.debug(f"생성된 솔루션: {solution}")
        return solution
    except Exception as e:
        logger.error(f"솔루션 생성 중 오류 발생: {e}")
        return "솔루션 생성 중 오류가 발생했습니다."

