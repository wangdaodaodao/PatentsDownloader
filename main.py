# -*- coding: utf-8 -*-
"""
    作者:     王导导
    版本:     2.0
    日期:     2020/05/23
    项目名称： 专利下载
"""


import webbrowser



import os
from pickle import TRUE
import time

from config import *
from patentdetail import *
from patentdown import *

if __name__ == "__main__":
    print()
    isStop = False
    isDown = True
    isCheck = True
    while not isStop:
        input_word = input('请选择：\n0.关键词查询专利\n1.已经有专利号直接下载\3.e退出程序\n请输入>>:')
        if input_word == str(0):
            
            keywords = input('请输入要查询关键词：')
            url = 'https://s.wanfangdata.com.cn/patent?q={patent_keywords}'.format(patent_keywords=keywords)
            webbrowser.open(url)
            
            select_2 = input('1.输入专利号下载专利\n2.下载本页所有专利\n请选择：')
            if select_2 == str(1):
                input_pantent_no = input('请输入专利号吧:')
                get_pantent_pdf(input_pantent_no)

                isStop = True
            else:
                print('不好意思哟,等在等待功能完善!')
                isStop = True

        elif input_word == str(1):
            keywords = input('请输入专利号：')
            # 引入False主要是为了事先只有专利号下载的方式
            get_pantent_pdf(keywords, False)
            # 跳出循环
            isStop = True
        
            while isCheck:
                if choice == 'N' or choice == 'n':
                    isCheck = False
                    isDown = False
                    isStop = True
                    print('已退出程序。')
                elif choice == 'Y' or choice == 'y':
                    int_page += 1
                    break
                else:
                    choice = input('输入错误重新输入（Y或者N）:')

        elif input_word == 'e':
            isStop = True
            print('已退出')
        elif input_word == 'E':
            isStop = True
            print('已退出')
        else:
            print('输入错误请重新输入1或者2。')
