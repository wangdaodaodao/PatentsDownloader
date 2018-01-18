import requests
from bs4 import BeautifulSoup
import lxml

base_url = 'http://g.wanfangdata.com.cn/search/searchList.do?searchType=patent&pageSize=50&page={page_nums}&searchWord={patants_keywords}&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all'


def get_id(patant_keywords, page_nums):
    response = requests.get(base_url.format(
        patants_keywords='助洗剂', page_nums=1))
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.select('.share_summary')
    patants_id = list(set([i.get('onclick').split('=')[2].split("'")[
                      0] for i in soup.select('.stitle')]))
    return patants_id
