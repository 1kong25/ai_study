import pytesseract
import cv2 #cv2.COLOR_BGR2GRAY옵션으로 그레이 스케일로 변환
# 이미지 경로: /Users/kjh001/Downloads/aitest.jpeg

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
config = ('-l kor+eng --oem 3 --psm 4') 
img=cv2.imread("/Users/kjh001/Downloads/aitest.jpeg")
# cv2.imshow("ori",img) #이미지 띄우기
print(pytesseract.image_to_string(img,config=config))

print("===========그레이스케일 변환 후==========")

img_gray=cv2.imread("/Users/kjh001/Downloads/aitest.jpeg",cv2.IMREAD_GRAYSCALE)
print(pytesseract.image_to_string(img_gray,config=config))

