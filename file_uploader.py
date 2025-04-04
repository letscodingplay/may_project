from PIL import Image
import streamlit as st

uploaded_file = st.file_uploader("이미지 파일을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드한 이미지', use_column_width=True)
