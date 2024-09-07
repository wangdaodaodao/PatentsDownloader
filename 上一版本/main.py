# -*- coding: utf-8 -*-
"""
    项目名称： 专利下载
    作者:     王导导
    版本:     2.1
    日期:     2024/09/07
    更新内容:  增加了菜单系统，改进了用户交互
    

    上一版本:  2.0
    上一日期:  2020/05/23
"""


import webbrowser
import os
import time
import urllib.parse  # 添加这行导入

from config import *
from patentdetail import *
from patentdown import *

def main_menu():
    while True:
        print("\n------主菜单------")
        print("0. *关键词*查询专利")
        print("1. *已有专利号*直接下载")
        print("2. 退出程序")
        choice = input("请选择 (0/1/2): ")

        if choice == '0':
            keyword_search_menu()
        elif choice == '1':
            direct_download_menu()
        elif choice == '2':
            print("程序已退出")
            break
        else:
            print("无效选择，请重新输入")

def keyword_search_menu():
    while True:
        keywords = input('请输入要查询--关键词-- (输入 "b" 返回主菜单, "q" 退出程序): ')
        if keywords.lower() == 'b':
            return
        elif keywords.lower() == 'q':
            print("程序已退出")
            exit()

        encoded_keywords = urllib.parse.quote(keywords)
        url = f'https://s.wanfangdata.com.cn/patent?q={encoded_keywords}'
        webbrowser.open(url)

        while True:
            print("\n1. **输入专利号**下载专利")
            print("2. 下载本页所有专利 (功能待完善)")
            print("3. 返回**关键词搜索**")
            print("4. 返回**主菜单**")
            print("5. 退出程序")
            select_2 = input('请选择 (1/2/3/4/5): ')

            if select_2 == '1':
                input_patent_no = input('请输入专利号: ')
                get_pantent_pdf(input_patent_no)
            elif select_2 == '2':
                print('不好意思哟,等在等待功能完善!')
            elif select_2 == '3':
                break
            elif select_2 == '4':
                return
            elif select_2 == '5':
                print("程序已退出")
                exit()
            else:
                print("无效选择，请重新输入")

def direct_download_menu():
    while True:
        patent_no = input('请输入--专利号-- (输入 "b" 返回主菜单, "q" 退出程序): ')
        if patent_no.lower() == 'b':
            return
        elif patent_no.lower() == 'q':
            print("程序已退出")
            exit()

        get_pantent_pdf(patent_no)

        choice = input('是否继续下载其他专利? (y/n): ')
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    main_menu()
