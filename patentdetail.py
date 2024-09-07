import json

import blackboxprotobuf
import requests

# 定义请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;,',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
    'Content-Type': 'application/grpc-web+proto',
}

# 定义基础URL模板
BASE_URL = 'https://s.wanfangdata.com.cn/patent?q={patent_keywords}&p={page_nums}'

def get_patent_number(keywords, page_num=1):
    """
    获取专利号
    :param keywords: 搜索关键词
    :param page_num: 页码数，默认为1
    """
    url = 'https://s.wanfangdata.com.cn/SearchService.SearchService/search'
    
    # 定义请求数据
    request_data = {
        "1": [
            {
                "1": "patent",
                "2": keywords,
                "5": page_num,
                "6": "2",
                "8": "\u0000"
            }
        ]
    }
    
    # 定义消息类型
    message_type = {
        '1': {'type': 'message', 
              'message_typedef': {
                                    '1': {'type': 'bytes', 'name': ''},
                                    '2': {'type': 'bytes', 'name': ''}, 
                                    '5': {'type': 'int', 'name': ''}, 
                                    '6': {'type': 'bytes', 'name': ''}, 
                                    '8': {'type': 'bytes', 'name': ''}}, 
              'name': ''}, 
        '0': {'type': 'bytes', 'name': ''}, 
        '2': {'type': 'bytes', 'name': ''}
    }

    # 编码请求数据
    encoded_data = bytes(blackboxprotobuf.encode_message(request_data, message_type))
    bytes_header = bytes([0, 0, 0, 0, len(encoded_data)])

    # 发送请求并解析响应
    response = requests.post(url, headers=headers, data=bytes_header + encoded_data)
    response_data, _ = blackboxprotobuf.protobuf_to_json(response.content[5:-20])
    json_data = json.loads(response_data)
    patent_list = json_data.get('4', [])

    # 打印搜索URL和专利号
    print(BASE_URL.format(patent_keywords=keywords, page_nums=page_num))
    for patent in patent_list:
        print(patent.get('119'))

# 示例调用
# get_patent_number('琼脂糖', 5)
