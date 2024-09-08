# -*- coding: utf-8 -*-
"""
    项目名称： 专利下载
    作者:     王导导
    版本:     3.0
    日期:     2024/09/08
    更新内容:  增加了下载本页所有专利的功能
    

    上一版本:  2.2
    上一日期:  2024/09/07
"""


import webbrowser
import os
import time
import urllib.parse  
import re

from config import *
from patentdetail import get_pantent_info
from patentdown import get_pantent_pdf, download_all_patents, DIR_PATH
from utils import open_search_page, validate_patent_number,check_local_patent,print_menu



def main_menu():
    while True:
        options = {
            "1": "*关键词*查询专利",
            "2": "*已有专利号*直接下载",
            "3": "退出程序"
        }
        print_menu("主菜单", options)
        choice = input("请选择操作 (1-3): ")

        if choice == '1':
            keyword_search_menu()
        elif choice == '2':
            direct_download_menu()
        elif choice == '3':
            print("程序已退出")
            break
        else:
            print("无效选择，请重新输入")

def keyword_search_menu():
    while True:
        keywords = input('\n请输入要查询的关键词 (输入 "b" 返回主菜单, "q" 退出程序): ')
        if keywords.lower() == 'b':
            return
        elif keywords.lower() == 'q':
            print("程序已退出")
            exit()

        # open_search_page(keywords)
        current_page = 1

        while True:
            patents = get_pantent_info(keywords, current_page)

            print(f"\n当前专利查询关键词: {keywords}")
            print(f"当前页面: {current_page}")
            print("\n当前页专利信息列表：")
            for i, patent in enumerate(patents, 1):
                print(f"{i}. {patent['专利号']} - {patent['标题']}")

            options = {
                "0": "下载所有专利",
                "1-N": "下载对应编号的专利",
                "X": "下一页",
                "S": "上一页",
                "R": "返回关键词搜索",
                "M": "返回主菜单",
                "Q": "退出程序"
            }
            print_menu("选项", options)
            choice = input("请选择 (0/1-N/X/S/R/M/Q): ").upper()

            if choice == '0':
                successful, failed = download_all_patents(keywords)
                print(f"批量下载完成。成功: {successful}, 失败: {failed}")
            elif choice.isdigit() and 1 <= int(choice) <= len(patents):
                patent = patents[int(choice) - 1]
                try:
                    print(f"[Step1.]准备下载>>: {patent['标题']} ")
                    get_pantent_pdf(patent['专利号'])
                    print(f"[Step5.]完成下载>>: {patent['标题']} ({patent['专利号']})")
                except Exception as e:
                    print(f"下载失败: {patent['标题']} ({patent['专利号']}). 错误: {str(e)}")
            elif choice == 'X':
                current_page += 1
            elif choice == 'S':
                if current_page > 1:
                    current_page -= 1
                else:
                    print("已经是第一页了")
            elif choice == 'R':
                break
            elif choice == 'M':
                return
            elif choice == 'Q':
                print("程序已退出")
                exit()
            else:
                print("无效选择，请重新输入")

def direct_download_menu():
    while True:
        patent_no = input("请输入专利号（输入'q'返回上级菜单）：")
        if patent_no.lower() == 'q':
            break
        
        validation_result = validate_patent_number(patent_no)
        if validation_result is True:
            # 检查本地是否已存在该专利文件
            local_file = check_local_patent(patent_no)
            if local_file:
                print(f"专利文件已存在: {local_file}")
                continue  # 继续下一次循环，要求输入新的专利号
            
            # 如果本地不存在，则尝试下载
            print(f"正在尝试下载专利: {patent_no}")
            if get_pantent_pdf(patent_no):
                print(f"成功下载专利: {patent_no}")
            else:
                print(f"未能下载专利: {patent_no}")
        else:
            print(f"专利号格式错误: {validation_result}")



if __name__ == "__main__":
    main_menu()
