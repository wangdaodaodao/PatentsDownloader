import json
import re

import blackboxprotobuf
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;,',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
    'Content-Type': 'application/grpc-web+proto',

}


# 获取专利号,传入的参数为关键词， 页码数
base_url = 'https://s.wanfangdata.com.cn/patent?q={patent_keywords}&p={page_nums}'


def get_patent_nuber(keywords, page_nums):
    url = 'https://s.wanfangdata.com.cn/SearchService.SearchService/search'
    deserialize_data = {
        "1": [
            {
                "1": "patent",
                "2": keywords,
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
    jj = json.loads(response_data)
    tt = jj.get('4')
    print(base_url.format(patent_keywords=keywords, page_nums=page_nums))
    for j in tt:
        print(j.get('119'))


get_patent_nuber('琼脂糖', 5)
