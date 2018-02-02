import re
import os
import sys
import requests

from config import *
from patentid import *
from pdfdown import *
session = requests.Session()

verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'
securepdf_url = 'http://{host_name}/cnpat/SecurePdf.aspx'

# 由专利号直接下载专利


def get_pdf(patent_no='CN201510708735.4'):
    # 获得验证码
    data_verify = {
        'cnpatentno': patent_no,
        'Common': '1'
    }
    response_verify = session.post(
        verify_url, headers=headers_verify, data=data_verify)
    response_verifycode = session.get(verifycode_url)
    with open('yzm.jpg', 'wb') as code:
        code.write(response_verifycode.content)
    os.system('start yzm.jpg')
    yzm = input('输入验证码：>>')
    os.remove('yzm.jpg')

    # 搜索界面
    data_search = {
        'cnpatentno': patent_no,
        'common': '1',
        'ValidCode': yzm,
    }

    response_search = session.post(
        search_url, data=data_search, headers=headers_search)
    if '错误' in response_search.text:
        print(response_search.text)

    elif '专利号' in response_search.text:
        tips_pattern = re.compile('<td>(.*?)</td>')
        print(tips_pattern.findall(response_search.text)[0])
    else:
        print('正在获取专利信息并下载：')

        pattern = re.compile('<input name="PatentNo" value="(.*?)" type="hidden" /><input name="Name" value="(.*?)" type="hidden" /><input name="PatentType" value="(.*?)" type="hidden" /><input name="PageNumFM" value="(.*?)" type="hidden" /><input name="UrlFM" value="(.*?)" type="hidden" /><input name="PageNumSD" value="(.*?)" type="hidden" /><input name="UrlSD" value="(.*?)"type="hidden"  /><input name="PublicationDate" value="(.*?)" type="hidden" /><input name="ReadyType" value="(.*?)" type="hidden" /><input name="FulltextType" value="(.*?)" type="hidden" /><input name="Common" value="(.*?)" type="hidden" /></form>')
        search_data = list(pattern.findall(response_search.text)[0])
        host_pattern = re.compile('{document.Download.action="(.*?)"')
        host_name = host_pattern.findall(response_search.text)[
            3].split('//')[1].split('/')[0]
        FulltextType_pattern = re.compile(
            'document.Download.FulltextType.value="(.*?)"')
        FulltextType_value = FulltextType_pattern.findall(response_search.text)[
            3]

        # 下载网页界面
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

        headers_securepdf['Host'] = host_name
        response_securepdf = session.post(securepdf_url.format(
            host_name=host_name), headers=headers_securepdf, data=data_securepdf)

        # pdf文件下载
        file_url = 'http://{url}/cnpat/package/%E5%8F%91%E6%98%8E%E4%B8%93%E5%88%A9%E7%94%B3%E8%AF%B7%E8%AF%B4%E6%98%8E%E4%B9%A6{numbers}.pdf'
        dir_path = '.' + os.sep + 'pdf'
        try:
            os.mkdir(dir_path)
        except Exception as e:
            # print('{}已存在'.format(dir_path))
            pass
        file_name = dir_path + os.sep + '{name}.pdf'

        if not os.path.exists(file_name):
            down_file(file_url.format(url=host_name, numbers=patent_no),
                      file_name.format(name=patent_no))
        else:
            print('已存在')
