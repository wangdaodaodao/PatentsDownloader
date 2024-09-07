# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     2.1
    日期:     2024/09/07
    项目名称： 通过专利号,在药物在线网站下载专利
"""

import os
import platform
import re
import sys
import time
from urllib.parse import unquote, quote
import subprocess
import requests
import click
from config import *

# 创建会话对象，用于保持连接
session = requests.Session()

# 定义常用URL
VERIFY_URL = 'http://www2.drugfuture.com/cnpat/verify.aspx'
VERIFYCODE_URL = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
SEARCH_URL = 'http://www2.drugfuture.com/cnpat/search.aspx'
SECUREPDF_URL = 'http://{host_name}/cnpat/SecurePdf.aspx'

# 创建保存PDF的目录
DIR_PATH = os.path.join(os.getcwd(), 'pdf')
os.makedirs(DIR_PATH, exist_ok=True)

dir_path = os.getcwd() + os.sep + 'pdf'
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

def open_image(image_path):
    """
    跨平台打开图片文件
    """
    system = platform.system()

    if system == 'Darwin':  # macOS
        subprocess.call(('open', image_path))
    elif system == 'Windows':  # Windows
        os.startfile(image_path)
    else:  # Linux 和其他系统
        try:
            subprocess.call(('xdg-open', image_path))
        except FileNotFoundError:
            # 如果 xdg-open 不可用，尝试使用其他常见的图片查看器
            viewers = ['display', 'feh', 'eog', 'xv']
            for viewer in viewers:
                try:
                    subprocess.call((viewer, image_path))
                    break
                except FileNotFoundError:
                    continue
            else:
                print("无法打开图片文件。请手动打开：", image_path)

def get_yzm(patent_no):
    while True:
        data_verify = {
            'cnpatentno': patent_no,
            'Common': '1' }
        response_verify = session.post(verify_url, headers=headers_verify, data=data_verify)
        response_verifycode = session.get(verifycode_url)
        
        # 保存验证码图片
        yzm_path = 'yzm.png'
        with open(yzm_path, 'wb') as code:
            code.write(response_verifycode.content)
        
        # 打开验证码图片
        open_image(yzm_path)

        yzm = input('输入验证码：>>')
        data_search = {
            'cnpatentno': patent_no,
            'common': '1',
            'ValidCode': yzm, }
        response_search = session.post(search_url, data=data_search, headers=headers_search)
        if '错误' in response_search.text:
            print(response_search.text)
        elif '专利号' in response_search.text:
            tips_pattern = re.compile('<td>(.*?)</td>')
            return None
        else:
            return response_search.text

def get_pdf_info(response):
    FulltextType_pattern = re.compile('document.Download.FulltextType.value="(.*?)"')
    FulltextType_value = FulltextType_pattern.findall(response)[3]
    host_name_pattern = re.compile('{document.Download.action="(.*?)"')
    host_name = host_name_pattern.findall(response)[4].split('//')[1].split('/')[0]

    headers_securepdf['Host'] = host_name
    pattern = re.compile('<input name="PatentNo" value="(.*?)" type="hidden" /><input name="Name" value="(.*?)" type="hidden" /><input name="PatentType" value="(.*?)" type="hidden" /><input name="PageNumFM" value="(.*?)" type="hidden" /><input name="UrlFM" value="(.*?)" type="hidden" /><input name="PageNumSD" value="(.*?)" type="hidden" /><input name="UrlSD" value="(.*?)"type="hidden"  /><input name="PublicationDate" value="(.*?)" type="hidden" /><input name="ReadyType" value="(.*?)" type="hidden" /><input name="FulltextType" value="(.*?)" type="hidden" /><input name="Common" value="(.*?)" type="hidden" /></form>')
    search_data = list(pattern.findall(response)[0])
    # 下载专利网页界面
    data_securepdf = {
        'PatentNo': search_data[0],
        'Name': search_data[1],
        'PatentType': search_data[2],
        'PageNumFM': search_data[3],
        'UrlFM': search_data[4],
        'PageNumSD': search_data[5],
        'UrlSD': search_data[6],
        'PublicationDate': search_data[7],
        'ReadyType': search_data[8],
        'FulltextType': FulltextType_value,
        'Common': search_data[10],
    }
    response_securepdf = session.post(securepdf_url.format(
        host_name=host_name), headers=headers_securepdf, data=data_securepdf)
    if 'wgsj' in data_securepdf.get('PatentType'):
        type_name = '外观设计专利授权说明书'
    elif 'fmzl' in data_securepdf.get('PatentType'):
        type_name = '发明专利申请说明书'
    elif 'syxx' in data_securepdf.get('PatentType'):
        type_name = '实用新型专利申请说明书'
    file_url = 'http://{url}/cnpat/package/{type_name}CN{numbers}.pdf'.format(
        url=host_name, type_name=quote(type_name), numbers=data_securepdf.get('PatentNo'))
    
    # 对文件名进行 URL 编码
    encoded_name = quote(data_securepdf.get('Name'))
    p_name = '{name}-CN{number}.pdf'.format(name=encoded_name, number=data_securepdf.get('PatentNo'))
    file_name = dir_path + os.sep + p_name
    return file_name, file_url

def smart_unquote(s):
    """智能解码URL编码的字符串"""
    while '%' in s:
        s = unquote(s)
    return s

import shutil
from tqdm import tqdm

def down_pdf(name, url):
    """下载PDF文件并显示进度"""
    new_filename = smart_unquote(name)
    new_path = os.path.join(DIR_PATH, os.path.basename(new_filename))

    if os.path.exists(new_path):
        print('文件已存在')
        return new_path

    response = session.get(url, headers=headers_securepdf, stream=True)
    length = int(response.headers.get('content-length', 0))
    
    with open(new_path, 'wb') as code, tqdm(
        desc=f'下载专利<{os.path.basename(new_filename)}>',
        total=length,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = code.write(chunk)
            progress_bar.update(size)
    
    if os.path.getsize(new_path) < 10000:
        print('下载失败：文件大小异常')
        os.remove(new_path)
        return None

    return new_path

def get_pantent_pdf(patent_no):
    resp = get_yzm(patent_no)
    if resp:
        info = get_pdf_info(resp)
        actual_path = down_pdf(info[0], info[1])
        print(f"文件已保存至: {actual_path}")
    else:
        print('抱歉,无法查询到专利,请检查专利号是否正确')