import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
config = ('-l kor+eng --oem 3 --psm 4') # psm은 page segmentation modes 5x /best:4(구조 그대로 나옴), 11(인식한 거 한 줄로 나옴)
print(pytesseract.image_to_string("/Users/kjh001/Desktop/study/ai_tes_pic/aitest.jpeg",config=config))