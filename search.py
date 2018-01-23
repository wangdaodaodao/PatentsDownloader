import requests
from patentid import *
from config import *
from verify import *



def search_patent(name='CN201510708735.4'):
    url = 'http://www2.drugfuture.com/cnpat/search.aspx'
    data = {
        'cnpatentno':name,
        'common':'1',
        'ValidCode':verifyCode(),
    }

    response = requests.get(url, data=data, headers=headers_verifycode)
    print(response.text)


search_patent()