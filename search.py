import requests
from patentid import *
from config import *
import re


session = requests.Session()
no = 'CN201510708735.4'

verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'


def verifyCode():
    data = {
    'cnpatentno':no,
    'Common':'1'
    }
    response_1 = session.post(verify_url, headers=headers_verify, data =data )


    response_2 = session.get(verifycode_url)
    with open('yzm.jpg', 'wb') as code:
        code.write(response_2.content)
    yzm = input('输入验证：>>')

    return yzm






def search_patent():
 
    data = {
        'cnpatentno':no,
        'common':'1',
        'ValidCode':verifyCode(),
    }

    response = session.post(search_url, data=data, headers=headers_search)
    print(response.text)

    pattern = re.compile('(.*?)')

search_patent()