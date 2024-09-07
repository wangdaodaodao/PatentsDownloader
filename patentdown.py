# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     2.0
    日期:     2022/06/14
    项目名称： 通过专利号,在药物在线网站下载专利

"""

import os
import platform
import re
import shutil
import time
import urllib
import sys
import requests

import click
from config import *
from pdfdown import *

session = requests.Session()

verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'
securepdf_url = 'http://{host_name}/cnpat/SecurePdf.aspx'

dir_path = os.getcwd() + os.sep + 'pdf'
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

#查询专利前需要处理验证码页面
def get_yzm(patent_no):
    while True:
        data_verify = {
            'cnpatentno': patent_no,
            'Common': '1' }
        response_verify = session.post(verify_url, headers=headers_verify, data=data_verify)
        response_verifycode = session.get(verifycode_url)
        with open('yzm.jpg', 'wb') as code:
            code.write(response_verifycode.content)
        
        if platform.system() == 'Windows':
            os.system('start yzm.jpg')

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
            break
        else:
            print('[{}]验证码正确，准备获取专利信息'.format(time.strftime('%m.%d %H:%M:%S',time.localtime())))
            return response_search.text
            break

#通过验证码后的页面response包含专利信息
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
        type_name = urllib.parse.unquote('外观设计专利授权说明书')
    elif 'fmzl' in data_securepdf.get('PatentType'):
        type_name = urllib.parse.unquote('发明专利申请说明书')
    elif 'syxx' in data_securepdf.get('PatentType'):
        type_name = urllib.parse.unquote('实用新型专利申请说明书')
    file_url = 'http://{url}/cnpat/package/{type_name}CN{numbers}.pdf'.format(
        url=host_name, type_name=type_name, numbers=data_securepdf.get('PatentNo'))
    p_name = '{name}-CN{number}.pdf'.format(name=urllib.parse.unquote(
        data_securepdf.get('Name')), number=data_securepdf.get('PatentNo'))
    file_name = dir_path + os.sep + p_name
    print('[{}]已经获取到pdf文件地址并准备下载：'.format(time.strftime('%m.%d %H:%M:%S',time.localtime())))
    # print(p_name, file_url)
    return file_name, file_url



def download_pdf(file_name, file_url):
    """下载PDF文件，检查是否已存在，并验证下载是否成功"""
    try:
        # 获取远程文件信息
        response = session.head(file_url, headers=headers_securepdf)
        remote_size = int(response.headers.get('content-length', 0))
        remote_name = os.path.basename(file_name)

        # 检查本地文件是否存在
        if os.path.exists(file_name):
            local_size = os.path.getsize(file_name)
            local_name = os.path.basename(file_name)

            # 比较文件大小和名称
            if local_size == remote_size and local_name == remote_name:
                print(f'文件 {local_name} 已存在，停止下载。')
                return

        # 下载文件
        response = session.get(file_url, headers=headers_securepdf, stream=True)
        response.raise_for_status()  # 如果请求不成功，抛出异常
        length = int(response.headers.get('content-length', 0))
        label = '正在下载专利<{}>,{:.2f}Kb'.format(os.path.basename(file_name), length/1024)
        print(label)
        
        downloaded = 0
        with open(file_name, 'wb') as code:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    code.write(chunk)
                    downloaded += len(chunk)
                    progress = int(50 * downloaded / length) if length else 0
                    sys.stdout.write('\r[{}{}] {:.1f}%'.format('=' * progress, ' ' * (50 - progress), 100 * downloaded / length if length else 0))
                    sys.stdout.flush()
        print()  # 打印一个换行，移动到下一行

        # 验证下载是否成功
        if os.path.getsize(file_name) < 10000:
            print('下载失败：文件大小异常')
            os.remove(file_name)
        else:
            print(f'文件 {os.path.basename(file_name)} 下载成功。')

    except requests.RequestException as e:
        print(f'下载失败：{str(e)}')
        if os.path.exists(file_name):
            os.remove(file_name)
    except Exception as e:
        print(f'发生未知错误：{str(e)}')
        if os.path.exists(file_name):
            os.remove(file_name)

# down_pdf_file('1.deb','https://files.cnblogs.com/files/wangdaodao/deb.zip')
def down_pdf(name, url):
    if not os.path.exists(name):
        response = session.get(url, headers=headers_securepdf)
        length = int(response.headers.get('content-length'))
        label = '正在下载专利<{}>,{:.2f}Kb'.format(name.split('/')[-1], length/1024)
        with click.progressbar(length=length, label=label) as progressbar:
            with open(name, 'wb') as code:  # 下载文件
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        code.write(chunk)
                        progressbar.update(1024)
    else:
        print('文件已存在！')
    if os.path.getsize(name) < 10000:
        print('下载失败')
        os.remove(name)



def get_pantent_pdf(patent_no):
    resp = get_yzm(patent_no)
    if resp:
        info = get_pdf_info(resp)

        
        download_pdf(info[0], info[1])
    else:
        print('抱歉,无法查询到专利,请检查专利号是否正确')




