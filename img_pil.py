from PIL import Image

# 이미지 열기
img = Image.open("img/sample01.jpg")

# 이미지 정보 출력
print(img.format, img.size, img.mode)

# 이미지 보여주기
img.show()

# 이미지 저장하기
img.save("new_image.png")
