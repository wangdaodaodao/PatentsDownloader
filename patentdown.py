# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     1.0
    日期:     2019/02/11
    项目名称： 专利下载

"""

import re,time
import os
import urllib
import click
import shutil
import requests
import platform
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


def get_yzm(patent_no):
    while True:
        data_verify = {
            'cnpatentno': patent_no,
            'Common': '1'
        }
        response_verify = session.post(
            verify_url, headers=headers_verify, data=data_verify)
        # print(response_verify.text)
        response_verifycode = session.get(verifycode_url)
        with open('yzm.jpg', 'wb') as code:
            code.write(response_verifycode.content)
        if platform.system() == 'Windows':
            os.system('start yzm.jpg')
        yzm = input('输入验证码：>>')
        data_search = {
            'cnpatentno': patent_no,
            'common': '1',
            'ValidCode': yzm,
        }
        # print('正在查询专利信息。。。')
        response_search = session.post(
            search_url, data=data_search, headers=headers_search)
        if '错误' in response_search.text:
            print(response_search.text)
        elif '专利号' in response_search.text:
            tips_pattern = re.compile('<td>(.*?)</td>')
            print(tips_pattern.findall(response_search.text)[0])
            return None
            break
        else:
            print('验证码正确，获得网页查询页面信息')
            return response_search.text
            break


def get_pdf_info(response):
    FulltextType_pattern = re.compile(
        'document.Download.FulltextType.value="(.*?)"')
    FulltextType_value = FulltextType_pattern.findall(response)[3]
    host_name_pattern = re.compile('{document.Download.action="(.*?)"')
    host_name = host_name_pattern.findall(
        response)[3].split('//')[1].split('/')[0]
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
    print('已经获取到pdf文件地址，')
    # print(p_name, file_url)
    return file_name, file_url


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
        shutil.move(name)


def get_pdf(patent_no, patent_name):
    # if os.path.exists()
    resp = get_yzm(patent_no)
    if resp:
        info = get_pdf_info(resp)
        # print(info)
        if patent_name:
            file_name = dir_path + os.sep + patent_name
            down_pdf(file_name, info[1])
        else:
            print(info[0])
            # print(patent_name,info[0])


            down_pdf(info[0], info[1])


# get_pdf('CN201510708735.4', '1.pdf')
# get_pdf('CN201510708735.4', False)