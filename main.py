import PyPDF2
import pdfplumber
from pdfminer.high_level import extract_text

import os
# import pytesseract
from PIL import Image

import easyocr
from pdf2image import convert_from_path


pdf = "S.E.Lain_PSX_Game_English_Translation _v0.1_7Jun2014.pdf"
txt = "output.txt"


def pypdf2_f(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text()
        
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

def pdfplumber_f(pdf_path, txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        
        for page in pdf.pages:
            text += page.extract_text()
        
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

def pdfminer_f(pdf_path, txt_path):
    text = extract_text(pdf_path)
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# pypdf2_f(pdf, txt)
# pdfplumber_f(pdf, txt)
# pdfminer_f(pdf, txt)


poppler_path = "C:\Program Files\Tesseract-OCR\tesseract.exe"

def pdf_ocr_to_text(pdf_path, txt_path, poppler_path):
    """
    将图片型PDF转换为文本
    
    参数:
        poppler_path: Windows系统需要提供poppler的bin路径
    """
    # Step 1: 将PDF转换为图片列表
    images = convert_from_path(pdf, poppler_path=poppler_path)
    
    # Step 2: 识别每张图片中的文字
    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 中英文识别
        full_text += f"--- 第 {i+1} 页 ---\n{text}\n\n"
    
    # Step 3: 保存文本
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

# 使用示例：
# Windows用户需要设置poppler路径（如：r"C:\path\to\poppler-xx\bin"）
# 和tesseract路径（如：pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe')
# 以及添加中文语言包（下载chi_sim.traineddata放到Tesseract的tessdata目录）

pdf_ocr_to_text(pdf, "output.txt", poppler_path)



def pdf_easyocr_to_text(pdf_path, txt_path, poppler_path=None):
    # 初始化EasyOCR阅读器（中文+英文）
    reader = easyocr.Reader(['ch_sim', 'en'])
    
    # 转换PDF为图片
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    
    full_text = ""
    for i, image in enumerate(images):
        # 将PIL图像转换为RGB（EasyOCR需要）
        results = reader.readtext(image)
        page_text = "\n".join([result[1] for result in results])
        full_text += f"--- 第 {i+1} 页 ---\n{page_text}\n\n"
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

# pdf_easyocr_to_text(pdf, txt)

