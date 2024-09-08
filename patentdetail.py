import json,re

import blackboxprotobuf
import requests
from config import *


def decode_protobuf_message(data):
    # 移除前5个字节（可能是长度前缀）
    data = data[5:]
    
    # 查找所有专利号和标题
    patent_matches = re.findall(b'\n\x10(CN\d+\.\d+)\x12(.{1,200}?)\x1a', data)
    
    results = []
    
    for patent_number, title_bytes in patent_matches:
        patent_number = patent_number.decode('utf-8')
        title = title_bytes.decode('utf-8', errors='ignore').strip()
        
        # 移除HTML标签
        title = re.sub(r'<[^>]+>', '', title)
        
        # 移除所有非中文、非英文字母、非数字的字符，包括特殊符号和空白字符
        title = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', title)
        
        # 移除开头的单个英文字母（如果存在）
        title = re.sub(r'^[a-zA-Z]', '', title)
        
        results.append({
            "专利号": patent_number,
            "标题": title
        })
        
        # print(f"专利号: {patent_number}")
        # print(f"标题: {title}")
        # print()  # 添加空行以分隔不同的专利
    # print(results)
    return results

def get_pantent_info(keywords,pagenum):
    url = 'https://s.wanfangdata.com.cn/SearchService.SearchService/search'
    deserialize_data = {
        "1": [
            {
                "1": "patent",
                "2": keywords,
                "5": pagenum,
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

    form_data = bytes(blackboxprotobuf.encode_message(deserialize_data, message_type))
    bytes_head = bytes([0, 0, 0, 0, len(form_data)])
    response = requests.post(url, headers=headers_p_info, data=bytes_head+form_data)
    p_info = decode_protobuf_message(response.content)
    return p_info
