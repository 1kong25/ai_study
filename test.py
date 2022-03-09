import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
config = ('-l kor+eng --oem 3 --psm 11') 
print(pytesseract.image_to_string("/Users/kjh001/Downloads/aitest.jpeg",config=config))

