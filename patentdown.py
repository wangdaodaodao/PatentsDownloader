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
from utils import check_local_patent

from config import DIR_PATH  # 导入 DIR_PATH

from urllib.parse import unquote, quote

# 创建会话对象，用于保持连接
session = requests.Session()

# 定义常用URL
VERIFY_URL = 'http://www2.drugfuture.com/cnpat/verify.aspx'
VERIFYCODE_URL = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
SEARCH_URL = 'http://www2.drugfuture.com/cnpat/search.aspx'
SECUREPDF_URL = 'http://{host_name}/cnpat/SecurePdf.aspx'

# 创建保存PDF的目录
os.makedirs(DIR_PATH, exist_ok=True)

dir_path = os.getcwd() + os.sep + 'pdf'
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

def get_yzm(patent_no):
    """
    获取验证码并验证专利号。
    :param patent_no: 专利号
    :return: 验证后的响应文本或None
    """
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

        yzm = input('[Step2.]输入验证码（输入 "q" 退出当前专利下载，输入 "p" 退出所有专利下载）：>>')
        if yzm.lower() == 'q':
            return 'USER_EXIT'  # 用户选择退出当前专利下载
        elif yzm.lower() == 'p':
            return 'USER_EXIT_ALL'  # 用户选择退出所有专利下载

        data_search = {
            'cnpatentno': patent_no,
            'common': '1',
            'ValidCode': yzm, }
        response_search = session.post(SEARCH_URL, data=data_search, headers=headers_search)
        if '验证码输入错误，请返回重新输入。' in response_search.text:
            print('验证码错误，请重试')
        elif '专利号' in response_search.text:
            tips_pattern = re.compile('<td>(.*?)</td>')
            return None
        else:
            return response_search.text

def get_pdf_info(response):
    """
    从响应中提取PDF下载所需的信息。
    :param response: 验证后的响应文本
    :return: 文件名、文件URL、请求头和请求数据
    """
    # 提取 FulltextType 值
    FulltextType_pattern = re.compile('document.Download.FulltextType.value="(.*?)"')
    FulltextType_value = FulltextType_pattern.findall(response)[3]

    # 提取 host_name
    host_name_pattern = re.compile('{document.Download.action="(.*?)"')
    host_name = host_name_pattern.findall(response)[0].split('//')[1].split('/')[0]

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
    return file_name, file_url, headers, data_securepdf



def get_pantent_pdf(patent_no):
    """
    获取专利PDF文件。
    :param patent_no: 专利号
    :return: True 如果成功下载，False 如果失败, 'USER_EXIT' 如果用户选择退出当前专利下载, 'USER_EXIT_ALL' 如果用户选择退出所有专利下载
    """
    # 首先检查本地是否已存在文件
    local_file = check_local_patent(patent_no)
    if local_file:
        print(f"专利文件已存在: {local_file}")
        return True  # 文件已存在，无需下载

    while True:
        print(f"[Step1.]正在处理专利号: {patent_no}")
        try:
            resp = get_yzm(patent_no)
            if resp == 'USER_EXIT':
                return 'USER_EXIT'
            elif resp == 'USER_EXIT_ALL':
                return 'USER_EXIT_ALL'
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
    """
    提示用户是否重试操作。
    :return: True 如果用户选择重试，False 如果用户选择退出
    """
    while True:
        choice = input("是否重试？(Y/N): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("无效输入，请输入 Y 或 N")

def down_pdf(name, url, headers):
    """
    下载PDF文件并显示进度。
    :param name: 文件名
    :param url: 文件URL
    :param headers: 请求头
    :return: 文件路径或None
    """
    new_filename = smart_unquote(name)
    new_path = os.path.join(DIR_PATH, os.path.basename(new_filename))

    if os.path.exists(new_path):
        print('##文件已存在##')
        return new_path

    response = session.get(url, headers=headers, stream=True)
    length = int(response.headers.get('content-length', 0))
    
    with open(new_path, 'wb') as code, tqdm(
        desc=f'[Step3.2]正在下载>>',
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
    """
    下载本页所有专利。
    :param keywords: 查询关键词
    :return: 成功和失败的数量
    """
    patents = get_pantent_info(keywords, 1)  # 获取第一页的专利信息
    successful = 0
    failed = 0
    total_patents = len(patents)
    
    for index, patent in enumerate(patents, start=1):
        patent_no = patent["专利号"]
        title = patent["标题"]
        print("*" * 40)  # 分隔符
        print(f" 准备处理第 [{index}/{total_patents}] 个专利: {title} ({patent_no})")
        
        try:
            result = get_pantent_pdf(patent_no)
            if result == 'USER_EXIT':
                print(f"用户选择退出当前专利下载: {title} ({patent_no})")
                continue  # 继续处理下一个专利
            elif result == 'USER_EXIT_ALL':
                print("用户选择退出所有专利下载")
                break  # 终止所有专利下载
            elif result:
                print(f" 完成处理第 [{index}/{total_patents}] 个专利: {title} ({patent_no})")
                successful += 1
            else:
                print(f"处理失败: {title} ({patent_no})")
                failed += 1
        except Exception as e:
            print(f"处理失败: {title} ({patent_no}). 错误: {str(e)}")
            failed += 1
        
        time.sleep(1)  # 添加延迟以避免过快请求
    print("*" * 40)  # 分隔符
    print(f"处理完成。成功: {successful}, 失败: {failed}")
    return successful, failed