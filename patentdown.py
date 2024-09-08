# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     2.1
    日期:     2024/09/07
    项目名称： 通过专利号,在药物在线网站下载专利
"""

import os
import re
import sys
import time
import traceback

import requests
import click
from config import *

import shutil
from tqdm import tqdm

from patentdetail import get_pantent_info
from utils import open_image
from utils import smart_unquote
from utils import retry_or_exit

from urllib.parse import unquote, quote

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

def get_yzm(patent_no):
    while True:
        data_verify = {
            'cnpatentno': patent_no,
            'Common': '1' }
        response_verify = session.post(VERIFY_URL, headers=headers_verify, data=data_verify)
        response_verifycode = session.get(VERIFYCODE_URL)
        
        # 保存验证码图片
        yzm_path = 'yzm.png'
        with open(yzm_path, 'wb') as code:
            code.write(response_verifycode.content)
        
        # 打开验证码图片
        open_image(yzm_path)

        yzm = input('[Step2.]输入验证码（输入 "q" 退出）：>>')
        if yzm.lower() == 'q':
            return None  # 用户选择退出

        data_search = {
            'cnpatentno': patent_no,
            'common': '1',
            'ValidCode': yzm, }
        response_search = session.post(SEARCH_URL, data=data_search, headers=headers_search)
        if '错误' in response_search.text:
            print('验证码错误，请重试')
        elif '专利号' in response_search.text:
            tips_pattern = re.compile('<td>(.*?)</td>')
            return None
        else:
            return response_search.text

def get_pdf_info(response):

    # print(response)
    # 提取 FulltextType 值
    FulltextType_pattern = re.compile('document.Download.FulltextType.value="(.*?)"')
    FulltextType_value = FulltextType_pattern.findall(response)[3]

    # 提取 host_name
    host_name_pattern = re.compile('{document.Download.action="(.*?)"')

    host_name = host_name_pattern.findall(response)[0].split('//')[1].split('/')[0]
    print(host_name)
    # 提取所有需要的值
    pattern = re.compile('<input name="PatentNo" value="(.*?)" type="hidden" />'
                         '<input name="Name" value="(.*?)" type="hidden" />'
                         '<input name="PatentType" value="(.*?)" type="hidden" />'
                         '<input name="PageNumFM" value="(.*?)" type="hidden" />'
                         '<input name="UrlFM" value="(.*?)" type="hidden" />'
                         '<input name="PageNumSD" value="(.*?)" type="hidden" />'
                         '<input name="UrlSD" value="(.*?)"type="hidden"  />'
                         '<input name="PublicationDate" value="(.*?)" type="hidden" />'
                         '<input name="ReadyType" value="(.*?)" type="hidden" />'
                         '<input name="FulltextType" value="(.*?)" type="hidden" />'
                         '<input name="Common" value="(.*?)" type="hidden" />')
    search_data = list(pattern.findall(response)[0])
    print(search_data)
    # 构建请求数据
    data_securepdf = {
        'PatentNo': search_data[0],
        'Name': unquote(search_data[1]),  # 解码 URL 编码的名称
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

    # 构建 headers
    headers = {
        'Host': host_name,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 构建 URL
    url = f'http://{host_name}/cnpat/SecurePdf.aspx'

    # 确定文件类型和名称
    if 'wgsj' in data_securepdf['PatentType']:
        type_name = '外观设计专利授权说明书'
    elif 'fmzl' in data_securepdf['PatentType']:
        type_name = '发明专利申请说明书'
    elif 'syxx' in data_securepdf['PatentType']:
        type_name = '实用新型专利申请说明书'
    else:
        type_name = '未知类型专利说明书'

    file_url = f'http://{host_name}/cnpat/package/{type_name}CN{data_securepdf["PatentNo"]}.pdf'
    file_name = f'{data_securepdf["Name"]}-CN{data_securepdf["PatentNo"]}.pdf'
    print(file_url)
    return file_name, file_url, headers, data_securepdf

def check_local_patent(patent_no):
    """检查本地是否存在包含指定专利号的文件"""
    if not os.path.exists(DIR_PATH):
        return None

    patent_no = re.escape(patent_no)  # 转义特殊字符
    pattern = re.compile(rf'.*{patent_no}.*\.pdf', re.IGNORECASE)

    for filename in os.listdir(DIR_PATH):
        if pattern.match(filename):
            return os.path.join(DIR_PATH, filename)

    return None

def get_pantent_pdf(patent_no):
    # 首先检查本地是否已存在文件
    local_file = check_local_patent(patent_no)
    if local_file:
        print(f"专利文件已存在: {local_file}")
        return True  # 文件已存在，无需下载

    while True:
        print(f"[Step1.]正在处理专利号: {patent_no}")
        try:
            resp = get_yzm(patent_no)
            if resp is None:
                print("用户选择退出或无法查询到专利")
                return False
            
            print("[Step2.]成功获取验证码响应")
            info = get_pdf_info(resp)
            if info:
                file_name, file_url, headers, data_securepdf = info
                print(f"[Step3.]成功获取PDF信息: {file_name}")
                
                # 发送请求获取实际的下载链接
                response_securepdf = session.post(SECUREPDF_URL.format(host_name=headers['Host']), headers=headers, data=data_securepdf)
                if response_securepdf.status_code == 200:
                    result = down_pdf(file_name, file_url, headers)
                    if result:
                        print(f"[Step4.]文件已成功保存>>: {result}")
                        return True
                    else:
                        print("[错误] 下载PDF失败")
                else:
                    print(f"[错误] 获取下载链接失败，状态码: {response_securepdf.status_code}")
            else:
                print("[错误] 无法获取PDF信息")
        except ValueError as e:
            print(f"[数据错误] 在处理数据时发生错误: {str(e)}")
        except Exception as e:
            print(f"[未知错误] 发生未预期的错误:")
            print(traceback.format_exc())
        
        if not retry_or_exit():
            return False

def retry_or_exit():
    while True:
        choice = input("是否重试？(Y/N): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("无效输入，请输入 Y 或 N")

def down_pdf(name, url, headers):
    """下载PDF文件并显示进度"""
    new_filename = smart_unquote(name)
    new_path = os.path.join(DIR_PATH, os.path.basename(new_filename))

    if os.path.exists(new_path):
        print('##文件已存在##')
        return new_path

    response = session.get(url, headers=headers, stream=True)
    length = int(response.headers.get('content-length', 0))
    
    with open(new_path, 'wb') as code, tqdm(
        desc=f'[Step3.]正在下载>>',
        total=length,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = code.write(chunk)
            progress_bar.update(size)
    
    if os.path.getsize(new_path) < 10000:
        print('##下载失败##：文件大小异常')
        os.remove(new_path)
        return None

    return new_path

def download_all_patents(keywords):
    """下载本页所有专利"""
    patents = get_pantent_info(keywords, 1)  # 获取第一页的专利信息
    successful = 0
    failed = 0
    for patent in patents:
        patent_no = patent["专利号"]
        title = patent["标题"]
        print(f"[Step1.]准备处理>>: {title} ({patent_no})")
        try:
            if get_pantent_pdf(patent_no):
                print(f"[Step5.]完成处理>>: {title} ({patent_no})")
                successful += 1
            else:
                print(f"处理失败: {title} ({patent_no})")
                failed += 1
        except Exception as e:
            print(f"处理失败: {title} ({patent_no}). 错误: {str(e)}")
            failed += 1
        time.sleep(1)  # 添加延迟以避免过快请求
    print(f"处理完成。成功: {successful}, 失败: {failed}")
    return successful, failed

