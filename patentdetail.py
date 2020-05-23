import json
import re

import lxml
import requests
from bs4 import BeautifulSoup

base_url = 'http://g.wanfangdata.com.cn/search/searchList.do?searchType=patent&pageSize=50&page={page_nums}&searchWord={patent_keywords}&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all'
# 获取专利号,传入的参数为关键词， 页码数


def get_id(keywords='python', nums=1):
    patent_detail = []
    url = base_url.format(patent_keywords=keywords, page_nums=nums)
    # print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    detail = soup.select('.ResultCont')
    for a in detail:
        patents_info = {
            'patent_id': '',
            'patent_name': '',
            'patent_author': '',
        }
        text = str(a)
        id_pattern = re.compile('<span>CN(.*?)</span>')
        x = id_pattern.findall(text)
        if x:
            p_id = 'CN{}'.format(x[0])
        else:
            p_id = None
        
        name_pattern = re.compile('target="_blank">(.*?)</a>')
        y = name_pattern.findall(text)
        if y:
            p_name = y[0].replace('<em>', '').replace('</em>', '')

        author_pattern = re.compile('target="_blank">(.*?)</a></span>')
        z = author_pattern.findall(text)
        if z:
            p_author = z[0]
        else:
            p_author = '无法获取'
        patents_info['patent_id'] = p_id
        patents_info['patent_name'] = p_name
        patents_info['patent_author'] = p_author
        patent_details = patents_info
        # print(patents_info)
        if p_id:
            patent_detail.append(patent_details)

    return patent_detail


# for xxxx in (get_id('JAVA', 4)):
#     print(xxxx)
# # print(get_id('JAVA', 2))
