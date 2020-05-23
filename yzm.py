# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     1.0
    日期:     2019/02/11
    项目名称： 专利下载

"""

import os

from PIL import Image

import pytesser3
from patentdown import *

file_dir = os.getcwd() + os.sep + 'yzm.jpg'
im = Image.open(file_dir)

imgry = im.convert('L')
imgry.show()
