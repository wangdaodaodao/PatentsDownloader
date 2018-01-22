from patentid import *
from config import *
from bs4 import BeautifulSoup
import lxml
import requests


verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'


def verify(pantentno='CN200910083739.2'):

    data = {
        'cnpatentno': pantentno,
        'Common': '1'
    }

    response = requests.post(verify_url, headers=headers_verify, data = data)

    print(response)



verify()