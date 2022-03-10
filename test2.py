import pytesseract
import numpy as np
import cv2 # cv2.COLOR_BGR2GRAY옵션으로 그레이 스케일로 변환
# V1이미지 경로: /Users/kjh001/Desktop/study/ai_tes_pic/aitest.jpeg
# V2이미지(brighter) 경로: /Users/kjh001/Desktop/study/ai_tes_pic/aitest_brighter.jpeg
# 왜 밝은게 더 인식 잘 안 되는 걸까

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
config = ('-l kor+eng --oem 3 --psm 4') 
test_img="/Users/kjh001/Desktop/study/ai_tes_pic/aitest.jpeg"

img=cv2.imread(test_img)
# cv2.imshow("ori",img) #이미지 띄우기

print(pytesseract.image_to_string(img,config=config))

print("===========그레이스케일 변환 후==========")

def gray_scale(image):
    result=cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    # img_gray=cv2.cvtColor(img, cv2.COLOR_BAYER_BG2GRAY) // 왜 오류나는지 모르겠음
    return result
def img_threshold(image): # 이미지 임계처리 (이진화)
    # threshold(src,thresh,maxval,type) //thresh:임계값, maxval:임계값을 넘었을 때 적용할 value, type:thresholding type
    # thresholding type: cv2.THRESH_BINARY/cv2.THRESH_BINARY_INV/cv2.THRESH_TRUN/,cv2.THRESH_TOZERO/cv2.THRESH_TOZERO_INV
    result=cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return result
def remove_noise(image,kernel_size=5): # 노이즈제거 (커널 사이즈는 홀수로)
    result=cv2.medianBlur(image,ksize=kernel_size)
    return result

img_gray=gray_scale(test_img)
img=remove_noise(img_gray)
img=img_threshold(img) 
img=cv2.GaussianBlur(img,(3,3),0)

print(pytesseract.image_to_string(img,config=config))

