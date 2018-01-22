from patentid import *
from config import *
from bs4 import BeautifulSoup
import lxml
import requests
from PIL import Image
import pytesseract

verify_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'






def verifyCode():
    response = requests.get(verify_url, headers=headers_verifycode)
    with open('yzm.jpg', 'wb') as code:
        code.write(response.content)
    yzm = input('输入验证：>>')

    img = Image.open('yzm.jpg')
    vcode = pytesseract.image_to_string(img)
    print(vcode)
    return yzm

print(verifyCode())