import lxml
import requests
from bs4 import BeautifulSoup

from config import *


base_url = 'http://g.wanfangdata.com.cn/search/searchList.do?searchType=patent&pageSize=50&page={page_nums}&searchWord={patent_keywords}&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all'



# 获取专利号,传入的参数为关键词， 页码数
def get_id(keywords='python', page_nums=1):
    response = requests.get(base_url.format(
        patent_keywords=keywords, page_nums=page_nums))
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.select('.share_summary')
    patents_id = list(set([i.get('onclick').split('=')[2].split("'")[
                      0] for i in soup.select('.stitle')]))
    return patents_id
