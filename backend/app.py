# /backend/app.py

import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq, APIError
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app) 

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Groq 클라이언트 초기화
try:
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    app.logger.info("Groq client initialized successfully.")
except Exception as e:
    groq_client = None
    app.logger.error(f"Error initializing Groq client: {e}")

# 대상별 시스템 프롬프트 정의 (키를 소문자로 변경)
PROMPTS = {
    "upward": "You are a professional assistant for reporting to a superior. Convert the user's text into a polite, formal, and clear report format. Start with the conclusion first. Please write in Korean.",
    "lateral": "You are a helpful colleague. Convert the user's text into a friendly, mutually respectful tone for collaboration. Clearly state the request and deadline. Please write in Korean.",
    "external": "You are a customer service expert. Convert the user's text using the highest level of honorifics, emphasizing professionalism and a service-minded attitude. The result should be suitable for official announcements, apologies, or guidance. Please write in Korean."
}

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환을 위한 API 엔드포인트.
    Groq AI를 사용하여 실제 말투 변환을 수행합니다.
    """
    if not groq_client:
        app.logger.error("API call attempted but Groq client is not initialized.")
        return jsonify({"error": "Groq 클라이언트가 초기화되지 않았습니다. API 키를 확인하세요."}), 500

    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    # target 값을 소문자로 변환하여 일관성 유지
    target_lower = target.lower()

    if target_lower not in PROMPTS:
        return jsonify({"error": f"지원하지 않는 대상입니다: {target}"}), 400

    system_prompt = PROMPTS[target_lower]
    app.logger.info(f"Converting text for target '{target_lower}': {original_text[:50]}...")

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": original_text,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        
        converted_text = chat_completion.choices[0].message.content
        app.logger.info(f"Conversion successful for target '{target_lower}'.")

        response_data = {
            "original_text": original_text,
            "converted_text": converted_text,
            "target": target
        }
        
        return jsonify(response_data)

    except APIError as e:
        # Groq API 관련 오류 처리
        app.logger.error(f"Groq API error: {e}", exc_info=True)
        return jsonify({"error": "AI 모델을 호출하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 503
    except Exception as e:
        # 기타 서버 오류 처리
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": "서버에서 예기치 않은 오류가 발생했습니다."}), 500

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    