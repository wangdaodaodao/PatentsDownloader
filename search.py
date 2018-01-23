import requests
from patentid import *
from config import *
import re


session = requests.Session()


verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'
save_patent_url = 'http://www6.drugfuture.com/cnpat/SecurePdf.aspx'


def get_pdf(no = 'CN201410684364.6'):
    data_verify = {
        'cnpatentno': no,
        'Common': '1'
    }
    response_verify_1 = session.post(verify_url, headers=headers_verify, data=data_verify)
    response_verify_2 = session.get(verifycode_url)
    with open('yzm.jpg', 'wb') as code:
        code.write(response_verify_2.content)
    yzm = input('输入验证：>>')
    



    data_search = {
        'cnpatentno': no,
        'common': '1',
        'ValidCode': yzm,
    }
    response_search = session.post(search_url, data=data_search, headers=headers_search)
    pattern = re.compile('<input name="PatentNo" value=(.*?) type="hidden" /><input name="Name" value="(.*?)" type="hidden" /><input name="PatentType" value="(.*?)" type="hidden" /><input name="PageNumFM" value="(.*?)" type="hidden" /><input name="UrlFM" value="(.*?)" type="hidden" /><input name="PageNumSD" value="(.*?)" type="hidden" /><input name="UrlSD" value="(.*?)"type="hidden"  /><input name="PublicationDate" value="(.*?)" type="hidden" /><input name="ReadyType" value="(.*?)" type="hidden" /><input name="FulltextType" value="(.*?)" type="hidden" /><input name="Common" value="(.*?)" type="hidden" /></form>')
    tt =list( pattern.findall(response_search.text)[0])
    host_pattern = re.compile('{document.Download.action="(.*?)"')
    tt2 = host_pattern.findall(response_search.text)[2].split('//')[1].split('/')[0]
    


    
    data_savepdf = {
        'PatentNo':tt[0],
        'Name':tt[1],
        'PatentType':tt[2],
        'PageNumFM':tt[3],
        'UrlFM':tt[4],
        'PageNumSD':tt[5],
        'UrlSD':tt[6],
        'PublicationDate':tt[7],
        'ReadyType':tt[8],
        'FulltextType':tt[9],
        'Common':tt[10],
    }

    headers_save_patent['Host'] = tt2

    response_savepdf = session.post(save_patent_url, headers=headers_save_patent, data = data_savepdf)
    print(response_savepdf.text)
    headers_getpdf['Host'] = tt2
    headers_getpdf['Referer'] = 'http://{}/cnpat/SecurePdf.aspx'.format(tt2)

    file_url = 'http://{}/cnpat/package/%E5%8F%91%E6%98%8E%E4%B8%93%E5%88%A9%E7%94%B3%E8%AF%B7%E8%AF%B4%E6%98%8E%E4%B9%A6{}.pdf'.format(tt2, no)
    response_savepdf_2 = session.get(file_url, headers=headers_getpdf)


    print(file_url, headers_getpdf)
    with open('{}.pdf'.format(no), 'wb') as code:
        code.write(response_savepdf_2.content)
    print('下载完毕!!!')


get_pdf()

