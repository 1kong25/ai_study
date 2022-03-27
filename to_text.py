from PIL import Image
import pytesseract
import configparser
import cv2
import os

# config parser 초기화
config=configparser.ConfigParser()
# config 파일 읽기
config.read(os.path.dirname(os.path.realpath(__file__))+os.sep+'envs'+os.sep+'property.ini')

# 이미지에서 문자열 추출
def ocr(fullPath, outTxtPath, fileName,lang='kor'):
    img=Image.open(fullPath)
    txtName = os.path.join(outTxtPath, fileName.split('.')[0])
    # psm모드: https://github.com/tesseract-ocr/tesseract/wiki/Command-Line_Usage
    outText= pytesseract.image_to_string(img, lang=lang, config='--psm 1 -c preserve_interword_spaces=1')
    print(outText)
    toTxt(txtName,outText)

# 추출된 문자열 텍스트파일로 저장
def toTxt(txtName, outText):
    with open(txtName+".txt",'w',encoding='utf-8') as f:
        f.write(outText)

if __name__ == "__main__":
    # 텍스트 파일 저장 경로
    outTxtPath = os.path.dirname(os.path.realpath(__file__))+config['Path']['OcrTxtPath']
    
    # 현재 실행 파일 기준 하위 폴더의 모든 이미지 순회하며 추출
    for root,dirs,files in os.walk(os.path.dirname(os.path.realpath(__file__))+config['Path']['OriImgPath']):
        for fname in files:
            fullName=os.path.join(root,fname)
            ocr(fullName,outTxtPath,fname,'kor+eng')