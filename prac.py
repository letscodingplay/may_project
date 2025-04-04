import streamlit as st

st.title("안녕하세요!")
st.write("이건 정말 간단한 Streamlit 앱입니다.")

name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"환영합니다, {name}님!")