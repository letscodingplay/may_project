from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import requests
import torch

# 1. 이미지 가져오기
imgFile = "./img/sample07.jpg"  # 이미지 파일 경로
image = Image.open(imgFile)

# 2. 모델 및 프로세서 불러오기
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# 3. 이미지 전처리 및 모델 추론
inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# 4. 결과 후처리
target_sizes = torch.tensor([image.size[::-1]])  # (height, width)
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

# 5. 감지된 물체 출력
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    print(f"{model.config.id2label[label.item()]}: {round(score.item(), 3)} at {box.tolist()}")

# 6. 이미지에 박스 그리기
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    label_name = model.config.id2label[label.item()]
    draw.rectangle(box, outline="red", width=3)
    draw.text((box[0], box[1]), f"{label_name} {round(score.item(),2)}", fill="red", font=font)

# 7. 결과 보여주기
image.show()
image.save("output.jpg")  # 결과 이미지를 저장