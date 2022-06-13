from cgi import print_arguments
import json
import re
from traceback import print_tb
import blackboxprotobuf

import lxml
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;,',
    'Host': 's.wanfangdata.com.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
    'Content-Type': 'application/grpc-web+proto',
    'Origin': 'https://s.wanfangdata.com.cn',
    '-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
    'Referer': 'https://s.wanfangdata.com.cn/patent?q=java&p=2',

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
    print(soup.title)
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


def get_patent_nuber(keywords, page_nums):
    url = 'https://s.wanfangdata.com.cn/SearchService.SearchService/search'
    deserialize_data = {
        "1": [
            {
                "1": "patent",
                "2": keywords,
                # "9": "2",
                "5": page_nums,
                "6": "2",
                "8": "\u0000"
            }
        ]
    }
    message_type = {'1': {'type': 'message', 
                            'message_typedef': {
                                                '1': {'type': 'bytes', 'name': ''},
                                                '2': {'type': 'bytes', 'name': ''}, 
                                                '5': {'type': 'int', 'name': ''}, 
                                                '6': {'type': 'bytes', 'name': ''}, 
                                                '8': {'type': 'bytes', 'name': ''}}, 
                            'name': ''}, 
                    '0': {'type': 'bytes', 'name': ''}, 
                    '2': {'type': 'bytes', 'name': ''}}

    form_data = bytes(blackboxprotobuf.encode_message(
        deserialize_data, message_type))
    bytes_head = bytes([0, 0, 0, 0, len(form_data)])

    response = requests.post(url, headers=headers, data=bytes_head+form_data)

    response_data, response_type = blackboxprotobuf.protobuf_to_json(
        response.content[5:-20])
    # print(response_data)

    jj = json.loads(response_data)
    tt = jj.get('4')
    print(base_url.format(patent_keywords=keywords, page_nums=page_nums))
    for j in tt:
        print(j.get('119'))


get_patent_nuber('苹果', 10)
