# app/utils/ai_prediction.py

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import logging
from pathlib import Path

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 모델 파일 경로 설정 (상대 경로 사용)
BASE_DIR = Path(__file__).parent.parent  # utils 디렉토리의 상위 디렉토리 (app 디렉토리)
MODEL_PATH = BASE_DIR / 'models' / 'hairAI.h5'

logger.debug(f"모델 파일 경로: {MODEL_PATH}")
logger.debug(f"모델 파일 존재 여부: {MODEL_PATH.exists()}")

# 모델 로드
try:
    model = tf.keras.models.load_model(str(MODEL_PATH))
    logger.info("AI 모델 로드 성공")
except Exception as e:
    logger.error(f"AI 모델 로드 실패: {e}")
    model = None


def preprocess_image(img_path, target_size=(500, 500)):
    """
    이미지를 로드하고 전처리하여 모델에 입력할 수 있는 형태로 반환합니다.

    Parameters:
    - img_path (str): 이미지 파일의 경로
    - target_size (tuple): 이미지 리사이즈 크기

    Returns:
    - np.ndarray: 전처리된 이미지 배열
    """
    try:
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # 픽셀 값 정규화

        # 전처리된 이미지 저장 (디버깅 용도)
        processed_img_path = img_path.replace('.jpg', '_processed.jpg').replace('.jpeg', '_processed.jpeg').replace(
            '.png', '_processed.png')
        image.save_img(processed_img_path, img_array[0])
        logger.debug(f"전처리된 이미지 저장: {processed_img_path}")

        logger.debug(f"Preprocessed image shape: {img_array.shape}")
        return img_array
    except Exception as e:
        logger.error(f"이미지 전처리 중 오류 발생: {e}")
        raise


def calculate_score(probabilities, weights={'양호': 100, '경증': 50, '중증': 10}):
    """
    확률과 가중치를 기반으로 점수를 계산합니다.

    Parameters:
    - probabilities (list or np.ndarray): 각 클래스의 확률 [양호, 경증, 중증]
    - weights (dict): 각 클래스에 대한 가중치

    Returns:
    - float: 계산된 점수
    """
    try:
        score = (probabilities[0] * weights['양호']) + (probabilities[1] * weights['경증']) + (probabilities[2] * weights['중증'])
        logger.debug(f"점수 계산: (양호: {probabilities[0]} * {weights['양호']}) + "
                     f"(경증: {probabilities[1]} * {weights['경증']}) + "
                     f"(중증: {probabilities[2]} * {weights['중증']}) = {score}")
        return score
    except Exception as e:
        logger.error(f"점수 계산 중 오류 발생: {e}")
        return 0


def predict_image(img_array):
    """
    전처리된 이미지 배열을 입력받아 예측 결과와 확률을 반환합니다.
    경증일 경우 세분화된 단계를 추가로 반환합니다.

    Parameters:
    - img_array (np.ndarray): 전처리된 이미지 배열

    Returns:
    - dict: 예측 결과 클래스 및 각 클래스의 확률
    """
    if model is None:
        logger.error("AI 모델이 로드되지 않았습니다.")
        return {"prediction": "AI 모델이 로드되지 않았습니다.", "probabilities": [0, 0, 0], "score": 0}

    try:
        predictions = model.predict(img_array)
        logger.debug(f"예측 확률: {predictions}")

        predicted_class_index = np.argmax(predictions, axis=1)[0]

        # 클래스 인덱스와 라벨 매핑
        labels = {0: "양호", 1: "경증", 2: "중증"}
        predicted_label = labels.get(predicted_class_index, "Unknown")

        # 각 클래스별 확률 추출
        probabilities = predictions[0]
        healthy_prob = probabilities[0]  # 양호 확률
        mild_prob = probabilities[1]     # 경증 확률
        severe_prob = probabilities[2]   # 중증 확률

        logger.debug(f"클래스별 확률: [양호: {healthy_prob:.2f}, 경증: {mild_prob:.2f}, 중증: {severe_prob:.2f}]")

        # 점수 계산
        score = calculate_score(probabilities)

        # 경증 세분화 로직 적용
        if predicted_label == "경증":
            if mild_prob >= 0.6:
                predicted_label = "경증2단계"
                logger.debug("경증 확률이 0.6 이상이므로 경증2단계로 분류합니다.")
            else:
                if healthy_prob > severe_prob:
                    predicted_label = "경증1단계"
                    logger.debug("경증 확률이 0.6 미만이며, 양호 확률이 중증 확률보다 높으므로 경증1단계로 분류합니다.")
                else:
                    predicted_label = "경증3단계"
                    logger.debug("경증 확률이 0.6 미만이며, 중증 확률이 양호 확률보다 높으므로 경증3단계로 분류합니다.")

        # 초기 예측 클래스 출력
        logger.info(f"초기 예측 클래스: {predicted_label}")
        logger.info(f"계산된 점수: {score}")

        return {
            "prediction": predicted_label,
            "probabilities": probabilities.tolist(),
            "score": score
        }

    except Exception as e:
        logger.error(f"예측 중 오류 발생: {e}", exc_info=True)
        return {
            "prediction": f"예측 과정에서 오류 발생: {e}",
            "probabilities": [0, 0, 0],
            "score": 0
        }
