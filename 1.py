import pytesseract
from PIL import Image
# import tesserocr
 
im=Image.open('yzm.jpg')
print(pytesseract.image_to_string(im))
