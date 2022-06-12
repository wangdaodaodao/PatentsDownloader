import json
import re

import lxml
import requests
from bs4 import BeautifulSoup

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;,',
'Host': 's.wanfangdata.com.cn',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',

}


# 获取专利号,传入的参数为关键词， 页码数
base_url = 'https://s.wanfangdata.com.cn/patent?q={patent_keywords}&p={page_nums}'

def get_id(keywords='python', nums=1):
    patent_detail = []
    url = base_url.format(patent_keywords=keywords, page_nums=nums)
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    detail = soup.select('.title-id-hidden')
    # print(soup)
    print(detail)
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


get_id()