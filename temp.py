import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 가져오기
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer " + HUGGINGFACE_API_KEY}
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY 환경 변수가 설정되지 않았습니다.")

response = requests.get(API_URL, headers=headers)
print(response.status_code)
print(response.text)
