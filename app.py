import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64
from datetime import datetime
import uuid

# 페이지 설정
st.set_page_config(
    page_title="가족 감사 메시지 생성기",
    page_icon="❤️",
    layout="centered"
)

# 커스텀 CSS 적용
st.markdown("""
<style>
.font-family-1 {
    font-family: 'Arial', sans-serif;
}
.font-family-2 {
    font-family: 'Georgia', serif;
}
.font-family-3 {
    font-family: 'Verdana', sans-serif;
}
.font-family-4 {
    font-family: 'Courier New', monospace;
}
.font-size-small {
    font-size: 16px;
}
.font-size-medium {
    font-size: 20px;
}
.font-size-large {
    font-size: 24px;
}
.text-align-left {
    text-align: left;
}
.text-align-center {
    text-align: center;
}
.text-align-right {
    text-align: right;
}
.text-color-1 {
    color: #FF5733;
}
.text-color-2 {
    color: #33A1FF;
}
.text-color-3 {
    color: #33FF57;
}
.text-color-4 {
    color: #D433FF;
}
.card-template-1 {
    background: linear-gradient(135deg, #FFF5E6, #FFE0B2);
    border: 2px solid #FFD700;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
.card-template-2 {
    background: linear-gradient(135deg, #E6F5FF, #B2E0FF);
    border: 2px solid #4682B4;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
.card-template-3 {
    background: linear-gradient(135deg, #F5FFE6, #E0FFB2);
    border: 2px solid #228B22;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
.card-template-4 {
    background: linear-gradient(135deg, #FFE6F5, #FFB2E0);
    border: 2px solid #FF1493;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
.download-button {
    display: inline-block;
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    text-align: center;
    text-decoration: none;
    border-radius: 4px;
    font-weight: bold;
    margin-top: 10px;
}
.download-button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'generated_message' not in st.session_state:
    st.session_state.generated_message = None
if 'message_style' not in st.session_state:
    st.session_state.message_style = {
        'font_family': 'font-family-1',
        'font_size': 'font-size-medium',
        'text_align': 'text-align-center',
        'text_color': 'text-color-1',
        'template': 'card-template-1'
    }
if 'card_design' not in st.session_state:
    st.session_state.card_design = {
        'template': 'card-template-1',
        'layout': 'image_top',
        'add_date': True,
        'add_signature': True
    }
if 'final_card_image' not in st.session_state:
    st.session_state.final_card_image = None
if 'card_file_path' not in st.session_state:
    st.session_state.card_file_path = None

# 이미지 분석 함수 (데모 버전 - 실제 API 호출 없음)
def analyze_image(image):
    # 데모용 분석 결과
    demo_results = [
        {"label": "person", "score": 0.95},
        {"label": "person", "score": 0.92},
        {"label": "couch", "score": 0.85},
        {"label": "potted plant", "score": 0.78},
        {"label": "book", "score": 0.72},
        {"label": "cup", "score": 0.68}
    ]
    return demo_results

# 메시지 생성 함수 (데모 버전 - 실제 API 호출 없음)
def generate_message(analysis_results, recipient_type, tone, length):
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
    
    # 데모용 메시지 생성 (수신자 유형, 톤, 길이에 따라 다른 메시지)
    messages = {
        "어머니": {
            "감동적인": "어머니, 항상 저희 가족을 위해 헌신하시는 모습이 얼마나 감사한지 모릅니다. 사진 속에서 보이는 따뜻한 미소처럼, 어머니의 사랑은 언제나 우리 가족을 빛나게 합니다. 5월 가정의 달을 맞아 그 동안 표현하지 못했던 감사의 마음을 전합니다. 사랑합니다, 어머니.",
            "유쾌한": "우리 멋진 엄마! 항상 웃음이 가득한 우리 집의 분위기 메이커! 사진 속에서도 빛나는 엄마의 에너지가 느껴져요. 가끔은 잔소리도 하지만, 그 모든 것이 사랑이라는 거 알고 있어요. 5월 가정의 달, 엄마처럼 유쾌한 사람이 우리 가족에 있어 정말 행운이에요. 사랑해요!",
            "따뜻한": "어머니, 항상 가족을 위해 베푸시는 따뜻한 사랑에 감사드립니다. 사진 속에서 보이는 포근한 모습처럼, 어머니의 품은 언제나 저희에게 안식처가 됩니다. 5월 가정의 달을 맞아 평소에 표현하지 못했던 감사의 마음을 전합니다. 앞으로도 건강하게 오래오래 함께해 주세요."
        },
        "아버지": {
            "감동적인": "아버지, 언제나 묵묵히 가족을 위해 헌신하시는 모습이 얼마나 감사한지 모릅니다. 때로는 말씀이 적으셔도, 그 속에 담긴 깊은 사랑을 느낍니다. 사진 속에서 보이는 든든한 모습처럼, 아버지는 우리 가족의 큰 기둥입니다. 5월 가정의 달을 맞아 그 동안 표현하지 못했던 감사의 마음을 전합니다.",
            "유쾌한": "우리 집 슈퍼히어로 아빠! 항상 가족을 위해 애쓰시는 모습이 정말 멋져요. 사진 속에서도 아빠의 카리스마가 뿜뿜 넘치네요! 가끔은 엄격하시지만, 그 뒤에 숨겨진 따뜻한 마음 다 알고 있어요. 5월 가정의 달, 아빠처럼 멋진 사람이 우리 가족에 있어 정말 자랑스러워요!",
            "따뜻한": "아버지, 언제나 가족을 위해 애쓰시는 모습에 깊은 감사를 드립니다. 사진 속에서 보이는 든든한 모습처럼, 아버지는 우리 가족의 중심입니다. 때로는 말씀이 적으셔도, 그 행동으로 보여주시는 사랑이 얼마나 큰지 느낍니다. 5월 가정의 달을 맞아 평소에 표현하지 못했던 감사의 마음을 전합니다."
        },
        "가족 전체": {
            "감동적인": "우리 가족 모두에게, 함께하는 모든 순간이 얼마나 소중한지 다시 한번 느낍니다. 사진 속에 담긴 우리의 미소와 따뜻한 시간들이 제 인생에서 가장 값진 보물입니다. 서로 의지하고 사랑하며 만들어가는 우리 가족의 이야기가 앞으로도 계속되길 바랍니다. 5월 가정의 달을 맞아 모두에게 감사와 사랑을 전합니다.",
            "유쾌한": "세상에서 가장 특별한 우리 가족! 사진 속에서도 빛나는 우리만의 케미가 느껴지네요. 때로는 티격태격하지만, 그 속에서 피어나는 웃음과 사랑이 우리를 하나로 만들어줍니다. 5월 가정의 달, 이렇게 유쾌하고 사랑 넘치는 가족이 있어 매일이 축제 같아요. 우리 앞으로도 더 많은 추억 만들어가요!",
            "따뜻한": "사랑하는 우리 가족에게, 함께하는 모든 순간이 얼마나 소중한지 다시 한번 느낍니다. 사진 속에 담긴 우리의 미소와 따뜻한 시간들이 제 인생에서 가장 값진 보물입니다. 서로 의지하고 사랑하며 만들어가는 우리 가족의 이야기가 앞으로도 계속되길 바랍니다. 5월 가정의 달을 맞아 모두에게 감사와 사랑을 전합니다."
        }
    }
    
    # 기본값 설정
    if recipient_type not in messages:
        recipient_type = "가족 전체"
    if tone not in messages[recipient_type]:
        tone = "따뜻한"
    
    # 길이에 따른 메시지 조정
    message = messages[recipient_type][tone]
    if length == "짧은":
        # 첫 문장만 반환
        return message.split('.')[0] + "."
    elif length == "중간":
        # 절반 정도 반환
        sentences = message.split('.')
        half = len(sentences) // 2
        return '.'.join(sentences[:half+1])
    else:  # "긴"
        return message

# 스타일이 적용된 메시지 HTML 생성 함수
def get_styled_message_html(message, style):
    return f"""
    <div class="{style['template']}">
        <div class="{style['font_family']} {style['font_size']} {style['text_align']} {style['text_color']}">
            {message}
        </div>
    </div>
    """

# 디지털 카드 생성 함수
def create_digital_card(image, message, card_design, user_name):
    try:
        # 카드 크기 설정
        card_width, card_height = 800, 1000
        
        # 템플릿에 따른 배경색 설정
        background_colors = {
            'card-template-1': (255, 245, 230),  # 봄 햇살 테마
            'card-template-2': (230, 245, 255),  # 푸른 하늘 테마
            'card-template-3': (245, 255, 230),  # 신록의 숲 테마
            'card-template-4': (255, 230, 245)   # 벚꽃 향기 테마
        }
        
        border_colors = {
            'card-template-1': (255, 215, 0),    # 봄 햇살 테마
            'card-template-2': (70, 130, 180),   # 푸른 하늘 테마
            'card-template-3': (34, 139, 34),    # 신록의 숲 테마
            'card-template-4': (255, 20, 147)    # 벚꽃 향기 테마
        }
        
        bg_color = background_colors.get(card_design['template'], (255, 255, 255))
        border_color = border_colors.get(card_design['template'], (0, 0, 0))
        
        # 새 이미지 생성
        card = Image.new('RGB', (card_width, card_height), bg_color)
        draw = ImageDraw.Draw(card)
        
        # 테두리 그리기
        border_width = 10
        draw.rectangle(
            [(border_width, border_width), (card_width - border_width, card_height - border_width)],
            outline=border_color,
            width=border_width
        )
        
        # 레이아웃에 따라 이미지 배치
        # 이미지 크기 조정
        image_width = card_width - 100
        image_height = int(image.height * (image_width / image.width))
        resized_image = image.resize((image_width, image_height))
        
        if card_design['layout'] == 'image_top':
            # 이미지를 상단에 배치
            image_y = 50
            text_y = image_y + image_height + 30
        else:  # image_bottom
            # 이미지를 하단에 배치
            text_y = 50
            image_y = card_height - image_height - 50
        
        # 이미지 붙여넣기
        card.paste(resized_image, (50, image_y))
        
        # 텍스트 추가
        try:
            # 한글 폰트 로드 (WQY 폰트 사용)
            font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
            
            # 폰트 크기 설정 (더 크게 조정)
            title_font_size = 36
            body_font_size = 28
            footer_font_size = 24
            
            title_font = ImageFont.truetype(font_path, title_font_size)
            body_font = ImageFont.truetype(font_path, body_font_size)
            footer_font = ImageFont.truetype(font_path, footer_font_size)
            
            # 텍스트 줄바꿈 처리 (개선된 버전)
            max_width = card_width - 100  # 여백 고려
            lines = []
            
            # 제목 추가 (수신자에 따라 다른 제목)
            title = "5월 가정의 달 감사 메시지"
            title_width = draw.textlength(title, font=title_font)
            title_x = (card_width - title_width) / 2  # 중앙 정렬
            draw.text((title_x, text_y), title, fill=(0, 0, 0), font=title_font)
            
            # 본문 시작 위치
            text_y += title_font_size + 20
            
            # 본문 텍스트 줄바꿈 처리
            words = message.split()
            current_line = []
            current_width = 0
            
            for word in words:
                word_width = draw.textlength(word + " ", font=body_font)
                if current_width + word_width <= max_width:
                    current_line.append(word)
                    current_width += word_width
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # 본문 텍스트 그리기
            line_height = body_font_size + 10  # 줄 간격 추가
            for i, line in enumerate(lines):
                draw.text((50, text_y + i * line_height), line, fill=(0, 0, 0), font=body_font)
            
            # 날짜 및 서명 위치 계산
            footer_y = text_y + len(lines) * line_height + 30
            
            # 날짜 추가
            if card_design['add_date']:
                today = datetime.now().strftime("%Y년 %m월 %d일")
                draw.text((50, footer_y), today, fill=(100, 100, 100), font=footer_font)
            
            # 서명 추가
            if card_design['add_signature'] and user_name:
                signature = f"From. {user_name}"
                signature_width = draw.textlength(signature, font=footer_font)
                draw.text((card_width - 50 - signature_width, footer_y), signature, fill=(0, 0, 0), font=footer_font)
        
        except Exception as e:
            st.error(f"카드 텍스트 렌더링 중 오류 발생: {str(e)}")
            # 폰트 로드 실패 시 기본 폰트 사용 시도
            try:
                default_font = ImageFont.load_default()
                draw.text((50, text_y + 50), "폰트 로드 실패: " + str(e), fill=(255, 0, 0), font=default_font)
                draw.text((50, text_y + 80), message[:100] + "...", fill=(0, 0, 0), font=default_font)
            except:
                pass
        
        return card
    
    except Exception as e:
        st.error(f"카드 생성 중 오류 발생: {str(e)}")
        return None

# 이미지를 base64로 인코딩하는 함수
def get_image_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# 이미지 저장 함수
def save_image_to_file(image, file_name):
    try:
        # 저장 디렉토리 생성
        save_dir = "saved_cards"
        os.makedirs(save_dir, exist_ok=True)
        
        # 파일 경로 생성
        file_path = os.path.join(save_dir, file_name)
        
        # 이미지 저장
        image.save(file_path)
        
        return file_path
    except Exception as e:
        st.error(f"이미지 저장 실패: {str(e)}")
        return None

# 다운로드 링크 생성 함수
def get_download_link(image, file_name):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{file_name}" class="download-button">다운로드</a>'
    return href

# 진행 상태 표시 함수
def show_progress_bar():
    steps = ["사진 업로드", "이미지 분석", "메시지 생성", "스타일 설정", "카드 디자인", "저장"]
    current_step = 1
    
    if st.session_state.uploaded_image is not None:
        current_step = 2
    
    if st.session_state.analysis_results is not None:
        current_step = 3
    
    if st.session_state.generated_message is not None:
        current_step = 4
    
    if 'message_style' in st.session_state and st.session_state.message_style is not None:
        current_step = 5
    
    if st.session_state.final_card_image is not None:
        current_step = 6
    
    # 진행 상태 표시
    st.write("### 진행 상태")
    progress_html = '<div style="display: flex; justify-content: space-between; margin: 20px 0;">'
    
    for i, step in enumerate(steps, 1):
        if i < current_step:
            status_class = "completed"
            color = "#4CAF50"  # 완료: 녹색
        elif i == current_step:
            status_class = "current"
            color = "#2196F3"  # 현재: 파란색
        else:
            status_class = "pending"
            color = "#9E9E9E"  # 대기: 회색
        
        progress_html += f'<div style="background-color: {color}; color: white; padding: 8px 12px; border-radius: 20px; font-size: 14px;">{i}. {step}</div>'
    
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)
    st.divider()

# 제목 및 소개
st.title("가족 감사 메시지 생성기")
st.subheader("5월 가정의 달을 맞이하여 가족에게 감사의 마음을 전해보세요!")

st.write("""
이 앱은 여러분이 업로드한 가족 사진을 AI가 분석하고, 
분석 결과를 바탕으로 감동적인 감사 메시지를 생성해 드립니다.
생성된 메시지는 예쁜 디지털 카드로 만들어 저장할 수 있습니다.
""")

# 진행 상태 표시
show_progress_bar()

# 사용자 이름 입력
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
    
    # 이미지 표시
    st.image(image, caption="업로드된 가족 사진", use_column_width=True)
    
    # 이미지 분석 버튼
    if st.button("이미지 분석하기"):
        with st.spinner("이미지를 분석 중입니다..."):
            # 이미지 분석 실행 (데모 버전)
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
                # 메시지 생성 실행 (데모 버전)
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

    # 메시지 편집 및 스타일링 (생성된 메시지가 있을 때만 표시)
    if st.session_state.generated_message:
        st.write("### 메시지 편집 및 스타일링")
        
        # 메시지 편집
        edited_message = st.text_area(
            "메시지를 편집할 수 있습니다",
            value=st.session_state.generated_message,
            height=200
        )
        
        # 편집된 메시지 저장
        if edited_message != st.session_state.generated_message:
            st.session_state.generated_message = edited_message
            st.success("메시지가 편집되었습니다!")
        
        # 스타일링 옵션
        st.write("### 메시지 스타일 설정")
        
        # 2열 레이아웃
        col1, col2 = st.columns(2)
        
        with col1:
            # 폰트 패밀리 선택
            font_family = st.selectbox(
                "폰트 선택",
                [
                    ("Arial", "font-family-1"),
                    ("Georgia", "font-family-2"),
                    ("Verdana", "font-family-3"),
                    ("Courier New", "font-family-4")
                ],
                format_func=lambda x: x[0]
            )
            
            # 폰트 크기 선택
            font_size = st.selectbox(
                "폰트 크기",
                [
                    ("작게", "font-size-small"),
                    ("중간", "font-size-medium"),
                    ("크게", "font-size-large")
                ],
                format_func=lambda x: x[0]
            )
        
        with col2:
            # 텍스트 정렬 선택
            text_align = st.selectbox(
                "텍스트 정렬",
                [
                    ("왼쪽", "text-align-left"),
                    ("가운데", "text-align-center"),
                    ("오른쪽", "text-align-right")
                ],
                format_func=lambda x: x[0]
            )
            
            # 텍스트 색상 선택
            text_color = st.selectbox(
                "텍스트 색상",
                [
                    ("주황색", "text-color-1"),
                    ("파란색", "text-color-2"),
                    ("초록색", "text-color-3"),
                    ("보라색", "text-color-4")
                ],
                format_func=lambda x: x[0]
            )
        
        # 카드 템플릿 선택
        template = st.selectbox(
            "카드 템플릿",
            [
                ("봄 햇살", "card-template-1"),
                ("푸른 하늘", "card-template-2"),
                ("신록의 숲", "card-template-3"),
                ("벚꽃 향기", "card-template-4")
            ],
            format_func=lambda x: x[0]
        )
        
        # 스타일 적용 버튼
        if st.button("스타일 적용하기"):
            # 스타일 정보 저장
            st.session_state.message_style = {
                'font_family': font_family[1],
                'font_size': font_size[1],
                'text_align': text_align[1],
                'text_color': text_color[1],
                'template': template[1]
            }
            
            st.success("스타일이 적용되었습니다!")
        
        # 스타일이 적용된 메시지 미리보기
        st.write("### 스타일 미리보기")
        styled_message_html = get_styled_message_html(
            st.session_state.generated_message,
            st.session_state.message_style
        )
        st.markdown(styled_message_html, unsafe_allow_html=True)

        # 디지털 카드 디자인 옵션
        st.write("### 디지털 카드 디자인")
        
        # 레이아웃 선택
        st.write("#### 레이아웃 선택")
        layout = st.radio(
            "이미지 위치",
            [("이미지 상단", "image_top"), ("이미지 하단", "image_bottom")],
            format_func=lambda x: x[0]
        )
        st.session_state.card_design['layout'] = layout[1]
        
        # 추가 옵션
        st.write("#### 추가 옵션")
        col1, col2 = st.columns(2)
        
        with col1:
            add_date = st.checkbox("날짜 표시", value=st.session_state.card_design['add_date'])
            st.session_state.card_design['add_date'] = add_date
        
        with col2:
            add_signature = st.checkbox("서명 추가", value=st.session_state.card_design['add_signature'])
            st.session_state.card_design['add_signature'] = add_signature
        
        # 카드 생성 버튼
        if st.button("디지털 카드 생성하기"):
            with st.spinner("디지털 카드를 생성 중입니다..."):
                # 템플릿 정보 가져오기
                st.session_state.card_design['template'] = st.session_state.message_style['template']
                
                # 카드 생성
                final_card = create_digital_card(
                    st.session_state.uploaded_image,
                    st.session_state.generated_message,
                    st.session_state.card_design,
                    user_name
                )
                
                # 생성된 카드 저장
                if final_card:
                    st.session_state.final_card_image = final_card
                    st.success("디지털 카드가 생성되었습니다!")
        
        # 생성된 카드 표시
        if st.session_state.final_card_image:
            st.write("### 생성된 디지털 카드")
            st.image(st.session_state.final_card_image, caption="가족 감사 디지털 카드", use_column_width=True)
            
            # 저장 기능
            st.write("### 카드 저장하기")
            
            # 파일 이름 입력
            custom_file_name = st.text_input(
                "파일 이름 (확장자 제외)",
                value=f"가족_감사_카드_{datetime.now().strftime('%Y%m%d')}"
            )
            
            # 파일 형식 선택
            file_format = st.selectbox(
                "파일 형식",
                [("PNG", "png"), ("JPEG", "jpg")],
                format_func=lambda x: x[0]
            )
            
            # 저장 버튼
            if st.button("카드 저장하기"):
                # 파일 이름 생성
                file_name = f"{custom_file_name}.{file_format[1]}"
                
                # 이미지 저장
                file_path = save_image_to_file(st.session_state.final_card_image, file_name)
                
                if file_path:
                    st.session_state.card_file_path = file_path
                    st.success(f"카드가 성공적으로 저장되었습니다: {file_path}")
                    
                    # 다운로드 링크 생성
                    download_link = get_download_link(st.session_state.final_card_image, file_name)
                    
                    # 다운로드 링크 표시
                    st.markdown("아래 버튼을 클릭하여 카드를 다운로드하세요:", unsafe_allow_html=True)
                    st.markdown(download_link, unsafe_allow_html=True)
            
            # 새 카드 만들기 버튼
            if st.button("새 카드 만들기"):
                # 세션 상태 초기화
                st.session_state.uploaded_image = None
                st.session_state.analysis_results = None
                st.session_state.generated_message = None
                st.session_state.final_card_image = None
                st.session_state.card_file_path = None
                
                st.success("새 카드를 만들 준비가 되었습니다. 새 사진을 업로드해 주세요.")
                st.experimental_rerun()

# 이미지가 업로드되지 않은 경우 안내 메시지 표시
else:
    st.info("가족 사진을 업로드해 주세요.")

# 푸터
st.divider()
st.caption("© 2025 가족 감사 메시지 생성기 | 파이썬 프로젝트")
