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


def keywords_download(keywords):
    xx = get_id(keywords, 1)
    for x in xx:
        print(x.get('patent_id'))
        get_pdf(str(x.get('patent_id')))


if __name__ == "__main__":
    print()
    isstop = False
    isdown = True
    while not isstop:
        input_word = input('请选择：\n1.专利号下载\n2.关键词下载\n3.e退出程序\n请输入>>:')

        if input_word == str(1):
            keywords = input('请输入专利号：')
            get_pdf(keywords, False)
            isstop = True

        elif input_word == str(2):
            keywords = input('请输入关键词儿：')
            int_page = 1
            while isdown:
                patent_info = get_id(keywords, int_page)
                if not patent_info:
                    break
                # print(patent2_info)
                for p_detail in patent_info:
                    print(p_detail.get('patent_id'), p_detail.get('patent_author'), p_detail.get('patent_name'))
                    name = '{1}-{0}.pdf'.format(p_detail.get('patent_id'),p_detail.get('patent_name'))
                    get_pdf(p_detail.get('patent_id'),name )

                choice = input('第{}页下载完毕，是否继续下载请按Y或者N：'.format(int_page))

                if choice == 'N':
                    isstop = True
                    isdown = False
                    print('退出程序')

                elif choice == 'Y':
                    int_page += 1
                else:
                    print('输入错误！！！重新输入')
            print('222')
        elif input_word == 'e':
            isstop = True
            print('已退出')
        elif input_word == 'E':
            isstop = True
            print('已退出')
        else:
            print('重新选择，请输入1或者2。')
