import easyocr
import os
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pytesseract

print("程序开始执行")

# 检查 Python 和 EasyOCR 版本
import sys
print(f"Python 版本: {sys.version}")
print(f"EasyOCR 版本: {easyocr.__version__}")

# 检查图像文件
image_path = 'yzm.jpg'
print(f"图像路径: {os.path.abspath(image_path)}")

try:
    with Image.open(image_path) as img:
        print(f"图像成功打开，大小: {img.size}")
except Exception as e:
    print(f"打开图像时出错: {e}")
    sys.exit(1)

print("开始初始化 EasyOCR...")
reader = easyocr.Reader(['ch_sim','en'], verbose=True)
print("EasyOCR 初始化完成")

print("开始读取图像...")
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(img)

preprocessed_img = preprocess_image('yzm.jpg')
result = reader.readtext(image_path, 
                            allowlist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                            detail=0,
                            paragraph=False,
                            min_size=10,
                            contrast_ths=0.1,
                            adjust_contrast=0.5,
                            text_threshold=0.7,
                            low_text=0.4,
                            link_threshold=0.7)
print("图像读取完成")

print("识别结果：")
if result:
    for detection in result:
        text = detection[1]
        print(text)
else:
    print("没有识别到任何文本")

print("程序执行结束")

# 检查图像内容
img = Image.open('yzm.jpg')
plt.imshow(img)
plt.show()

# 使用 pytesseract 进行验证码识别
img = Image.open('yzm.jpg')
text = pytesseract.image_to_string(img)
print(text)