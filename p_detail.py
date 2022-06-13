import requests, lxml
from bs4 import BeautifulSoup


base_url = 'http://www.soopat.com/Home/Result?SearchWord={keywords}&FMZL=Y&SYXX=Y&WGZL=Y&FMSQ=Y&PatentIndex={pagenums}0&Valid=0'




resp = requests.get(base_url.format(keywords='java', pagenums=2))
soup = BeautifulSoup(resp.text, 'lxml')

t = soup.select('.tooltiplink')

for t in t:
    a = t.get('sqh')
    print(a)

