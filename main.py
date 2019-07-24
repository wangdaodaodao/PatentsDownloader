# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     1.0
    日期:     2019/02/11
    项目名称： 专利下载

"""

from config import *
from patentdown import *
from patentid import *
import os


print('请选择：\n1：输入专利号下载\n2：输入关键词批量下载')
isDown = True
check = True

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
                if not os.path.exists('pdf' + os.sep + '{}.pdf'.format(i)):
                    print(i)
                    get_pdf(i)
                else:
                    print('专利{}已存在。'.format(i))
            while check:
                selection = input(
                    '第{}页下载完毕，按1或者2选择是否下载下一页：\n1为是，2为否：'.format(page_num))
                if selection == str(1):
                    page_num += 1
                    check = False
                elif selection == str(2):
                    isDown = False
                    print('取消下载！')
                    check = False
                else:
                    print('输入错误,重新输入！')
    else:
        print('关键词为空。')
else:
    print('输入错误请返回。')

