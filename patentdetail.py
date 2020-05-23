import lxml
import requests
import json
from bs4 import BeautifulSoup

base_url2 = 'http://g.wanfangdata.com.cn/search/searchList.do?searchType=patent&pageSize=50&page={page_nums}&searchWord={patent_keywords}&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all'
base_url = 'http://g.wanfangdata.com.cn/search/searchList.do?searchType=patent&pageSize=50&page={page_nums}&searchWord={patent_keywords}&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all'
# 获取专利号,传入的参数为关键词， 页码数

patents_id = []
def get_id(keywords='python', nums=1):
    url = base_url.format(patent_keywords=keywords, page_nums=nums)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.select('.summary')
    # print(soup, url)
    print(url)
    # print(title)
    id_in_soup = soup.select('.result_opera_export')
    for p_id in id_in_soup:
        if p_id:
            # print(p_id)
            print(p_id.get('docid'))
            patents_id.append(p_id.get('docid'))
    return patents_id


print(get_id('赵薇', 2))