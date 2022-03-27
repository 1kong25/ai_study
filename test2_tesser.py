import pytesseract
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform
#from imutils.contours import sort_contours
import re
#import requests

test_img="eggo_test.png"
image_nparray = np.asarray(bytearray(requests.get(test_img).content), dtype=np.uint8)
org_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR) 
 
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
config = ('-l kor+eng --oem 3 --psm 4') 

# img=cv2.imread(test_img)
# cv2.imshow("ori",img) #이미지 띄우기

def make_scan_image(image, width, ksize=(5,5), min_threshold=75, max_threshold=200):
    image_list_title = []
    image_list = []
    
    org_image = image.copy()
    image = imutils.resize(org_image, width=width)
    
    ratio = org_image.shape[1] / float(image.shape[1])
 
    # 이미지를 grayscale로 변환하고 blur를 적용
    # 모서리를 찾기위한 이미지 연산
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, ksize, 0)
    edged = cv2.Canny(blurred, min_threshold, max_threshold)
 
    image_list_title = ['gray', 'blurred', 'edged']
    image_list = [gray, blurred, edged]
 
    # contours를 찾아 크기순으로 정렬
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
 
    findCnt = None
 
    # 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
        # contours가 크기순으로 정렬되어 있기때문에 제일 첫번째 사각형을 영역으로 판단하고 break
        if len(approx) == 4:
            findCnt = approx
            break
 
        # 만약 추출한 윤곽이 없을 경우 오류
        if findCnt is None:
            raise Exception(("Could not find outline."))
 
 
        output = image.copy()
        cv2.drawContours(output, [findCnt], -1, (0, 255, 0), 2)
 
        image_list_title.append("Outline")
        image_list.append(output)
 
        # 원본 이미지에 찾은 윤곽을 기준으로 이미지를 보정
        transform_image = four_point_transform(org_image, findCnt.reshape(4, 2) * ratio)
    transform_image = convert_image(transform_image, image_type)
    
    return transform_image

scan_image = make_scan_image(org_image, width=200, ksize=(5, 5), min_threshold=20, max_threshold=100)

options = "--psm 4"
text = pytesseract.image_to_string(cv2.cvtColor(scan_image, cv2.COLOR_BGR2RGB), config=options)
 
# OCR결과 출력
print("[INFO] OCR결과:")
print("==================")
print(text)
print("\n")

def gray_scale(image):
    # img_gray=cv2.cvtColor(img, cv2.COLOR_BAYER_BG2GRAY) // 왜 오류나는지 모르겠음
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image): # 이미지 임계처리 (이진화)
    # threshold(src,thresh,maxval,type) //thresh:임계값, maxval:임계값을 넘었을 때 적용할 value, type:thresholding type
    # thresholding type: cv2.THRESH_BINARY/cv2.THRESH_BINARY_INV/cv2.THRESH_TRUN/,cv2.THRESH_TOZERO/cv2.THRESH_TOZERO_INV
    result=cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return result

def deskew(image): # 숫자 이미지를 읽어 기울어진 이미지 보정
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)    
    return rotated

deskew = deskew(img)
gray = gray_scale(deskew)
thresh = thresholding(gray)

### print(pytesseract.image_to_string(thresh, config=config))







