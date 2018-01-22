from patentid import *
from config import *
from bs4 import BeautifulSoup
import lxml
import requests


verify_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'

def verify(pantentno='CN200910083739.2'):

    data = {
        'cnpatentno': pantentno,
        'Common': '1'
    }

    response = requests.post(verify_url, headers=headers_verify, data = data)

    print(response)


def verifyCode():
    response = requests.get(verify_url, headers=headers_verifycode)
    with open('yzm.jpg', 'wb') as code:
        code.write(response.content)
    yzm = input('输入验证：>>')

    return yzm


print(verifyCode())