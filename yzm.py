# -*- coding: UTF-8 -*-
import os
import pytesser3
from patentdown import *
from PIL import Image


file_dir = os.getcwd() + os.sep + 'yzm.jpg'
im = Image.open(file_dir)

imgry = im.convert('L')
imgry.show()

