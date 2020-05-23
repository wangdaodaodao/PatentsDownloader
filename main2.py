# -*- coding: utf-8 -*-
"""
    作者:     王导导
    版本:     2.0
    日期:     2020/05/23
    项目名称： 专利下载
"""

import os

from config import *
from patentdetail import *
from patentdown import *

if __name__ == "__main__":
    print()
    isStop = False
    isDown = True
    isCheck = True
    while not isStop:
        input_word = input('请选择：\n1.专利号下载\n2.关键词下载\n3.e退出程序\n请输入>>:')
        if input_word == str(1):
            keywords = input('请输入专利号：')
            #引入False主要是为了事先只有专利号下载的方式
            get_pdf(keywords, False)
            #跳出循环
            isStop = True
        elif input_word == str(2):
            keywords = input('请输入关键词儿：')
            int_page = 1
            while isDown:
                patent_info = get_id(keywords, int_page)
                if not patent_info:
                    break
                for p_detail in patent_info:
                    print(p_detail.get('patent_id'), p_detail.get(
                        'patent_author'), p_detail.get('patent_name'))
                    name = '{1}-{0}.pdf'.format(p_detail.get('patent_id'),
                                                p_detail.get('patent_name'))
                get_pdf(p_detail.get('patent_id'), name)    
                choice = input('第{}页下载完毕，是否继续下载，请按Y或者N：'.format(int_page))
                while isCheck:    
                    if choice == 'N' or choice=='n':
                        isCheck = False                
                        isDown = False
                        isStop = True
                        print('已退出程序。')
                    elif choice == 'Y' or choice=='y':
                        int_page += 1
                        break
                    else:
                        choice=input('输入错误重新输入（Y或者N）:')
        elif input_word == 'e':
            isStop = True
            print('已退出')
        elif input_word == 'E':
            isStop = True
            print('已退出')
        else:
            print('重新选择，请输入1或者2。')
