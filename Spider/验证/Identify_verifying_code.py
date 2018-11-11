# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-10 10:21:16
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-10 10:33:04
import tesserocr
from PIL import Image

image = Image.open('code.jpg')
# 转化为灰度图像
image = image.convert('L')
threshold = 127
table=[]
for i in range(256):
    if i< threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table,'1')
result = tesserocr.image_to_text(image)
print(result.strip())