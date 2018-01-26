from config import *
from patentdown import *
from patentid import *

print('请选择：\n1：输入专利号下载\n2：输入关键词批量下载')

choice = input('输入1or2：')
if choice == str(1):
    number = input('输入专利号:')
    get_pdf(number)
elif choice == str(2):
    keywords = input('输入关键词:')
    for i in get_id(keywords):
            get_pdf(i)
else:
    print('输入错误请返回')
