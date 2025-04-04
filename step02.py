import streamlit as st
from PIL import Image
import io

# 페이지 설정 (이전 코드와 동일)
st.set_page_config(
    page_title="가족 감사 메시지 생성기",
    page_icon="❤️",
    layout="centered"
)

# 세션 상태 초기화 (앱 실행 시 한 번만 실행됨)
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

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

# 파일 업로더 구현
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
    st.write(f"이미지 형식: {image.format}")
    
    # 이미지 표시
    st.image(image, caption="업로드된 가족 사진", use_column_width=True)
    
    # 이미지 분석 버튼 (아직 기능 구현 전)
    if st.button("이미지 분석하기"):
        st.info("다음 차시에 이미지 분석 기능을 구현할 예정입니다.")

# 이미지가 업로드되지 않은 경우 안내 메시지 표시
else:
    st.info("가족 사진을 업로드해 주세요.")

# 푸터
st.divider()
st.caption("© 2025 가족 감사 메시지 생성기 | 파이썬 프로젝트")
