import streamlit as st
from PIL import Image
import io
import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 가져오기
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY 환경 변수가 설정되지 않았습니다.")

# 이미지 분석 함수
def analyze_image(image):
    # 이미지를 바이트로 변환
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Huggingface API 엔드포인트 (객체 감지 모델)
    API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
    
    # 헤더 설정
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    
    # API 요청
    try:
        response = requests.post(API_URL, headers=headers, data=img_byte_arr) 
        
        # 응답 확인
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 요청 실패: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API 요청 중 오류 발생: {str(e)}")
        return None

# 페이지 설정 (이전 코드와 동일)
st.set_page_config(
    page_title="가족 감사 메시지 생성기",
    page_icon="❤️",
    layout="centered"
)

# 세션 상태 초기화
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# 제목 및 소개 (이전 코드와 동일)
st.title("가족 감사 메시지 생성기")
st.subheader("5월 가정의 달을 맞이하여 가족에게 감사의 마음을 전해보세요!")

st.write("""
이 앱은 여러분이 업로드한 가족 사진을 AI가 분석하고, 
분석 결과를 바탕으로 감동적인 감사 메시지를 생성해 드립니다.
생성된 메시지는 예쁜 디지털 카드로 만들어 저장할 수 있습니다.
""")

# 구분선
st.divider()

# 사용자 이름 입력 (이전 코드와 동일)
user_name = st.text_input("당신의 이름을 입력하세요:")

if user_name:
    st.write(f"안녕하세요, {user_name}님! 가족 사진을 업로드해 보세요.")

# 파일 업로더 구현 (이전 코드와 동일)
st.write("### 사진 업로드")
uploaded_file = st.file_uploader("가족 사진을 선택하세요", type=["jpg", "jpeg", "png"])

# 이미지 처리 및 표시
if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)
    
    # 세션 상태에 이미지 저장
    st.session_state.uploaded_image = image
    
    # 이미지 정보 표시
    st.write(f"이미지 크기: {image.size[0]} x {image.size[1]} 픽셀")
    
    # 이미지 표시
    st.image(image, caption="업로드된 가족 사진", use_column_width=True)
    
    # 이미지 분석 버튼
    if st.button("이미지 분석하기"):
        with st.spinner("이미지를 분석 중입니다..."):
            # 이미지 분석 실행
            analysis_results = analyze_image(image)
            
            # 분석 결과 저장
            if analysis_results:
                st.session_state.analysis_results = analysis_results
                
                # 분석 결과 표시
                st.write("### 분석 결과")
                
                # 결과 시각화 (객체 감지 예시)
                detected_objects = []
                for obj in analysis_results:
                    label = obj['label']
                    score = obj['score']
                    if score > 0.7:  # 신뢰도 70% 이상만 표시
                        detected_objects.append(f"{label} ({score:.2f})")
                
                # 감지된 객체 목록 표시
                if detected_objects:
                    st.write("감지된 객체:")
                    for obj in detected_objects:
                        st.write(f"- {obj}")
                else:
                    st.write("감지된 객체가 없습니다.")
                
                # 분석 결과 요약
                st.write("### 분석 요약")
                summary = {
                    "인물 수": len([obj for obj in analysis_results if obj['label'] == 'person' and obj['score'] > 0.7]),
                    "주요 객체": ", ".join(set([obj['label'] for obj in analysis_results if obj['score'] > 0.8][:3])),
                    "장면 유형": "실내" if any(obj['label'] in ['couch', 'chair', 'dining table', 'bed'] for obj in analysis_results) else "실외"
                }
                
                # 요약 정보 표시
                for key, value in summary.items():
                    st.write(f"**{key}:** {value}")
                
                # 다음 단계 안내
                st.success("이미지 분석이 완료되었습니다! 다음 차시에 메시지 생성 기능을 구현할 예정입니다.")

# 이미지가 업로드되지 않은 경우 안내 메시지 표시
else:
    st.info("가족 사진을 업로드해 주세요.")

# 푸터
st.divider()
st.caption("© 2025 가족 감사 메시지 생성기 | 파이썬 프로젝트")
