import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="가족 감사 메시지 생성기",
    page_icon="❤️",
    layout="centered"
)

# 제목 및 소개
st.title("가족 감사 메시지 생성기")
st.subheader("5월 가정의 달을 맞이하여 가족에게 감사의 마음을 전해보세요!")

st.write("""
이 앱은 여러분이 업로드한 가족 사진을 AI가 분석하고, 
분석 결과를 바탕으로 감동적인 감사 메시지를 생성해 드립니다.
생성된 메시지는 예쁜 디지털 카드로 만들어 저장할 수 있습니다.
""")

# 구분선
st.divider()

# 사용자 이름 입력
user_name = st.text_input("당신의 이름을 입력하세요:")

if user_name:
    st.write(f"안녕하세요, {user_name}님! 가족 사진을 업로드해 보세요.")

# 파일 업로더 (아직 기능 구현 전)
st.write("### 사진 업로드")
st.info("다음 차시에 사진 업로드 기능을 구현할 예정입니다.")

# 버튼 (아직 기능 구현 전)
if st.button("메시지 생성하기"):
    st.success("버튼이 클릭되었습니다! 다음 차시에 실제 기능을 구현할 예정입니다.")

# 푸터
st.divider()
st.caption("© 2025 가족 감사 메시지 생성기 | 파이썬 프로젝트")