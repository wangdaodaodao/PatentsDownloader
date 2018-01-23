import re

import requests

from config import *
from patentid import *

session = requests.Session()


verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'


def get_pdf(no='CN201510708735.4'):
    data_verify = {
        'cnpatentno': no,
        'Common': '1'
    }
    response_verify = session.post(
        verify_url, headers=headers_verify, data=data_verify)
    response_verifycode = session.get(verifycode_url)
    with open('yzm.jpg', 'wb') as code:
        code.write(response_verifycode.content)
    yzm = input('输入验证：>>')

    data_search = {
        'cnpatentno': no,
        'common': '1',
        'ValidCode': yzm,
    }
    response_search = session.post(
        search_url, data=data_search, headers=headers_search)
    pattern = re.compile('<input name="PatentNo" value=(.*?) type="hidden" /><input name="Name" value="(.*?)" type="hidden" /><input name="PatentType" value="(.*?)" type="hidden" /><input name="PageNumFM" value="(.*?)" type="hidden" /><input name="UrlFM" value="(.*?)" type="hidden" /><input name="PageNumSD" value="(.*?)" type="hidden" /><input name="UrlSD" value="(.*?)"type="hidden"  /><input name="PublicationDate" value="(.*?)" type="hidden" /><input name="ReadyType" value="(.*?)" type="hidden" /><input name="FulltextType" value="(.*?)" type="hidden" /><input name="Common" value="(.*?)" type="hidden" /></form>')
    search_data = list(pattern.findall(response_search.text)[0])
    host_pattern = re.compile('{document.Download.action="(.*?)"')
    host_name = host_pattern.findall(response_search.text)[
        3].split('//')[1].split('/')[0]

    print()
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
        'FulltextType': search_data[9],
        'Common': search_data[10],
    }

    headers_securepdf['Host'] = host_name
    securepdf_url = 'http://{}/cnpat/SecurePdf.aspx'.format(host_name)
    print(securepdf_url, data_securepdf)
    response_securepdf = session.post(
        securepdf_url, headers=headers_securepdf, data=data_securepdf)

    headers_getpdf['Host'] = host_name
    headers_getpdf['Referer'] = 'http://{}/cnpat/SecurePdf.aspx'.format(
        host_name)

    file_url = 'http://{}/cnpat/package/%E5%8F%91%E6%98%8E%E4%B8%93%E5%88%A9%E7%94%B3%E8%AF%B7%E8%AF%B4%E6%98%8E%E4%B9%A6{}.pdf'.format(
        host_name, no)

    print(file_url)
    with open('{}.pdf'.format(no), 'wb') as code:
        code.write(session.get(file_url, headers=headers_getpdf).content)
    print('下载完毕!!!')


get_pdf()

# http://www10.drugfuture.com/cnpat/package/发明专利申请说明书CN201510708735.4.pdf
# http://www11.drugfuture.com/cnpat/package/发明专利申请说明书CN201510708735.4.pdf
