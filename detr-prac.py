from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import torch
colors = [
  "#FFFFFF",  # 하얀색
  "#33C1FF",  # 선명한 하늘색
  "#9D33FF",  # 보라
  "#33FF57",  # 연두색
  "#FF33A1",  # 핑크
  "#FFD133",  # 노랑
  "#335BFF",  # 푸른 파랑
  "#8DFF33",  # 연녹색
  "#FF3333",  # 빨강
  "#33FFF0",  # 시안
  "#B833FF",  # 보라+핑크
  "#FF8633",  # 주황+살구
  "#33FF88",  # 민트
  "#FF33D4",  # 핑크+보라
  "#33A1FF",  # 푸른 하늘색
  "#A6FF33",  # 연초록
  "#FF333F",  # 다홍
  "#33FFCC",  # 연한 시안
  "#CC33FF",  # 진보라
  "#FFAF33",  # 주황빛 노랑
  "#33FFD5",  # 밝은 민트
  "#FF33EC",  # 체리핑크
  "#33FF6E",  # 형광연두
  "#FF7F33",  # 다홍+주황
  "#33D4FF",  # 푸른 시안
  "#FF33B8",  # 핫핑크
  "#7EFF33",  # 형광초록
  "#FF3333",  # 강렬한 레드
  "#33E0FF",  # 파란 시안
  "#FF33C4"   # 마젠타
]
def anImage(imgFile):
# 1. 이미지 가져오기
# imgFile = "./img/sample03.jpg"  # 이미지 파일 경로
    image = Image.open(imgFile)

    # 2. 모델 및 프로세서 불러오기
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    # 3. 이미지 전처리 및 모델 추론
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # 4. 결과 후처리
    target_sizes = torch.tensor([image.size[::-1]])  # (height, width)
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.85)[0]
    
    print(results)
    
    # 5. 감지된 물체 출력
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        print(f"{model.config.id2label[label.item()]}: {round(score.item(), 3)} at {box.tolist()}")

    # 6. 이미지에 박스 그리기
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    num = 0
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        label_name = model.config.id2label[label.item()]
        draw.rectangle(box, outline=colors[num], width=20)
        draw.text((box[0], box[1]), f"{label_name} {round(score.item(),2)}", fill=colors[num], font=font)
        num += 1
    return 
# 7. 결과 보여주기
# image.show()
# image.save("output.jpg")  # 결과 이미지를 저장

imgFile = "./img/sample03.jpg"
anImage(imgFile)