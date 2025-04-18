import streamlit as st
from PIL import Image
import io
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 가져오기
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = OPENAI_API_KEY)

# 이미지 분석 함수 (이전 코드와 동일)
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

# 메시지 생성 함수
def generate_message(analysis_results, recipient_type, tone, length):
    try:
        # 분석 결과에서 주요 정보 추출
        detected_objects = []
        for obj in analysis_results:
            if obj['score'] > 0.7:
                detected_objects.append(obj['label'])
        
        # 중복 제거 및 문자열로 변환
        unique_objects = list(set(detected_objects))
        objects_str = ", ".join(unique_objects)
        
        # 인물 수 계산
        person_count = len([obj for obj in analysis_results if obj['label'] == 'person' and obj['score'] > 0.7])
        
        # 장면 유형 판단
        indoor_objects = ['couch', 'chair', 'dining table', 'bed', 'tv', 'laptop']
        outdoor_objects = ['car', 'tree', 'bicycle', 'bench', 'backpack']
        
        is_indoor = any(obj in unique_objects for obj in indoor_objects)
        is_outdoor = any(obj in unique_objects for obj in outdoor_objects)
        
        scene_type = "실내" if is_indoor and not is_outdoor else "실외" if is_outdoor and not is_indoor else "알 수 없음"
        
        # 프롬프트 작성
        prompt = f"""
- 사진에 있는 인물 수: {person_count}명
- 사진에서 감지된 객체: {objects_str}
- 장면 유형: {scene_type}
        
메시지 길이: {length}
형식: 5월 가정의 달을 맞이하여 {recipient_type}에게 보내는 감사 메시지
        """
        
        # OpenAI API 호출
        response = client.responses.create(
            model="gpt-3.5-turbo",
            instructions=f"""
당신은 5월 가정의 달을 맞이하여 가족에게 보내는 감사 메시지를 작성하는 AI입니다.
다음 정보를 바탕으로 {recipient_type}에게 보내는 감동적인 {tone} 메시지를 작성해주세요.
            """,
            input = prompt
        )
        
        # 생성된 메시지 반환
        return response.output_text
    
    except Exception as e:
        st.error(f"메시지 생성 실패: {str(e)}")
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
if 'generated_message' not in st.session_state:
    st.session_state.generated_message = None

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

# 이미지 처리 및 표시 (이전 코드와 동일)
if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)
    
    # 세션 상태에 이미지 저장
    st.session_state.uploaded_image = image
    
    # 이미지 정보 표시
    st.write(f"이미지 크기: {image.size[0]} x {image.size[1]} 픽셀")
    
    # 이미지 표시
    st.image(image, caption="업로드된 가족 사진", use_container_width =True)
    
    # 이미지 분석 버튼 (이전 코드와 동일)
    if st.button("이미지 분석하기"):
        with st.spinner("이미지를 분석 중입니다..."):
            # 이미지 분석 실행
            analysis_results = analyze_image(image)
            print(analysis_results)
            
            if analysis_results:
                st.session_state.analysis_results = analysis_results
                
                # 분석 결과 표시
                st.write("### 분석 결과")
                
                # 결과 시각화 (객체 감지 예시)
                detected_objects = []
                for obj in analysis_results:
                    label = obj['label']
                    score = obj['score']
                    if score > 0.9:  # 신뢰도 70% 이상만 표시
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
                    "인물 수": len([obj for obj in analysis_results if obj['label'] == 'person' and obj['score'] > 0.9]),
                    "주요 객체": ", ".join(set([obj['label'] for obj in analysis_results if obj['score'] > 0.8][:3])),
                    "장면 유형": "실내" if any(obj['label'] in ['couch', 'chair', 'dining table', 'bed'] for obj in analysis_results) else "실외"
                }
                
                # 요약 정보 표시
                for key, value in summary.items():
                    st.write(f"**{key}:** {value}")
                
                # 다음 단계 안내
                st.success("이미지 분석이 완료되었습니다!")

    # 메시지 생성 옵션 (분석 결과가 있을 때만 표시)
    if st.session_state.analysis_results:
        st.write("### 메시지 생성 옵션")
        
        # 수신자 유형 선택
        recipient_type = st.selectbox(
            "메시지 수신자를 선택하세요",
            ["어머니", "아버지", "할머니", "할아버지", "형제/자매", "가족 전체"]
        )
        
        # 메시지 톤 선택
        tone = st.selectbox(
            "메시지 톤을 선택하세요",
            ["감동적인", "유쾌한", "따뜻한", "진지한", "감성적인"]
        )
        
        # 메시지 길이 선택
        length = st.select_slider(
            "메시지 길이를 선택하세요",
            options=["짧은", "중간", "긴"]
        )
        
        # 메시지 생성 버튼
        if st.button("메시지 생성하기"):
            with st.spinner("감사 메시지를 생성 중입니다..."):
                # 메시지 생성 실행
                generated_message = generate_message(
                    st.session_state.analysis_results,
                    recipient_type,
                    tone,
                    length
                )
                
                # 생성된 메시지 저장 및 표시
                if generated_message:
                    st.session_state.generated_message = generated_message
                    
                    # 메시지 표시
                    st.write("### 생성된 감사 메시지")
                    st.write(generated_message)
                    
                    # 메시지 편집 옵션
                    edited_message = st.text_area(
                        "메시지를 편집할 수 있습니다",
                        value=generated_message,
                        height=200
                    )
                    
                    # 편집된 메시지 저장
                    if edited_message != generated_message:
                        st.session_state.generated_message = edited_message
                        st.success("메시지가 편집되었습니다!")
                    
                    # 다음 단계 안내
                    st.success("메시지 생성이 완료되었습니다!")

# 이미지가 업로드되지 않은 경우 안내 메시지 표시 (이전 코드와 동일)
else:
    st.info("가족 사진을 업로드해 주세요.")

# 푸터 (이전 코드와 동일)
st.divider()
st.caption("© 2025 가족 감사 메시지 생성기 | 파이썬 프로젝트")