from config import *
from patentdown import *
from patentid import *

print('请选择：\n1：输入专利号下载\n2：输入关键词批量下载')
isDown = True

choice = input('输入1or2：')
if choice == str(1):
    number = input('输入专利号:')
    get_pdf(number)
elif choice == str(2):
    keywords = input('输入关键词:')
    if keywords:
        page_num = 1
        while isDown:
            for i in get_id(keywords, page_num):
                    get_pdf(i)
            selection = input('第{}页现在完毕，按1或者2选择是否下载下一页：1为是，2为否'.format(page_num))
            if selection == str(1):
                page_num += 1                
            elif selection == str(2):
                isDown = False
                print('取消下载！')
            else:
                print('输入错误！')
    else:
        print('关键词为空')            
else:
    print('输入错误请返回')

