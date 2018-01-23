import requests
from patentid import *
from config import *
from verify import *


code = verifyCode('CN201510708735.4')
def search_patent(name='CN201510708735.4'):
    url = 'http://www2.drugfuture.com/cnpat/search.aspx'
    

    data = {
        'cnpatentno':name,
        'common':'1',
        'ValidCode':code,
    }

    response = requests.post(url, data=data, headers=headers_search)
    print(code)
    print(response.text)


search_patent()