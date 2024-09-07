# -*- coding: utf-8 -*-
"""
    文件名: captcha_solver.py
    功能: 处理中文验证码识别
    作者: [您的名字]
    日期: 2023/06/14
"""

import os
import pytesseract
from PIL import Image
import cv2
import numpy as np

# 设置 TESSDATA_PREFIX 环境变量
os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/share/tessdata/'

# 设置 Tesseract 命令路径
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def preprocess_image(image_path):
    # 读取图像
    img = cv2.imread(image_path)
    
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 二值化
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # 去噪
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # 膨胀
    dilation = cv2.dilate(opening, kernel, iterations=1)
    
    return dilation

def recognize_captcha(image_path):
    # 预处理图像
    processed_image = preprocess_image(image_path)
    
    # 使用Tesseract进行OCR，指定中文语言
    text = pytesseract.image_to_string(Image.fromarray(processed_image), lang='chi_sim', config='--psm 6')
    
    # 清理识别结果
    text = ''.join(c for c in text if '\u4e00' <= c <= '\u9fff')
    
    return text

def solve_captcha(image_path):
    try:
        captcha_text = recognize_captcha(image_path)
        print(f"识别的验证码: {captcha_text}")
        return captcha_text
    except Exception as e:
        print(f"验证码识别失败: {str(e)}")
        return None

if __name__ == "__main__":
    # 测试函数
    test_image = "yzm.jpg"  # 确保这个文件存在
    result = solve_captcha(test_image)
    if result:
        print(f"识别结果: {result}")
    else:
        print("验证码识别失败")