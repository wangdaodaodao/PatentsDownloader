import requests
from patentid import *
from config import *
import re


session = requests.Session()
no = 'CN201510708735.4'

verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'
save_patent_url = 'http://www6.drugfuture.com/cnpat/SecurePdf.aspx'


def verifyCode():
    data = {
        'cnpatentno': no,
        'Common': '1'
    }
    response_1 = session.post(verify_url, headers=headers_verify, data=data)
    response_2 = session.get(verifycode_url)
    with open('yzm.jpg', 'wb') as code:
        code.write(response_2.content)
    yzm = input('输入验证：>>')
    return yzm


def search_patent():
    data = {
        'cnpatentno': no,
        'common': '1',
        'ValidCode': verifyCode(),
    }
    response = session.post(search_url, data=data, headers=headers_search)
    pattern = re.compile('<input name="PatentNo" value=(.*?) type="hidden" /><input name="Name" value="(.*?)" type="hidden" /><input name="PatentType" value="(.*?)" type="hidden" /><input name="PageNumFM" value="(.*?)" type="hidden" /><input name="UrlFM" value="(.*?)" type="hidden" /><input name="PageNumSD" value="(.*?)" type="hidden" /><input name="UrlSD" value="(.*?)"type="hidden"  /><input name="PublicationDate" value="(.*?)" type="hidden" /><input name="ReadyType" value="(.*?)" type="hidden" /><input name="FulltextType" value="(.*?)" type="hidden" /><input name="Common" value="(.*?)" type="hidden" /></form>')
    tt =list( pattern.findall(response.text)[0])
    host_pattern = re.compile('{document.Download.action="(.*?)"')
    tt2 = host_pattern.findall(response.text)[2].split('//')[1].split('/')[0]
    return tt, tt2

def save_patent():
    tt = search_patent()
    data = {
        'PatentNo':tt[0][0],
        'Name':tt[0][1],
        'PatentType':tt[0][2],
        'PageNumFM':tt[0][3],
        'UrlFM':tt[0][4],
        'PageNumSD':tt[0][5],
        'UrlSD':tt[0][6],
        'PublicationDate':tt[0][7],
        'ReadyType':tt[0][8],
        'FulltextType':tt[0][9],
        'Common':tt[0][10],
    }

    headers_save_patent['Host'] = tt[1]

    print(headers_save_patent)
    response = session.post(save_patent_url, headers=headers_save_patent, data = data)

    file_url = 'http://{}/cnpat/package/%E5%8F%91%E6%98%8E%E4%B8%93%E5%88%A9%E7%94%B3%E8%AF%B7%E8%AF%B4%E6%98%8E%E4%B9%A6{}.pdf'.format(tt[1], no)
    response_2 = session.get(file_url)
    with open('{}.pdf'.format(no), 'wb') as code:
        code.write(response_2.content)
save_patent()

