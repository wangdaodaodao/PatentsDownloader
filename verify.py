from patentid import *
from config import *
from bs4 import BeautifulSoup
import lxml
import requests

verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
session = requests.Session()



def verifyCode(name='CN201510708735.4'):
    data = {
    'cnpatentno':name,
    'Common':'1'
    }
    response_1 = session.post(verify_url, headers=headers_verify, data =data )


    response_2 = session.get(verifycode_url, headers=headers_verifycode)
    with open('yzm.jpg', 'wb') as code:
        code.write(response_2.content)
    yzm = input('输入验证：>>')

    return yzm

