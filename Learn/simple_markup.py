# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-12 19:45:26
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-12 19:45:33
import sys
import re
import fileinput
from util import *
from handlers import HTMLRenderer

# title = True
# print('<body><html>')
# for block in blocks(fileinput.input()):
#     block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
#     if title:
#         print('<h1>')
#         print(block)
#         print('</h1>')
#         title = False
#     else:
#         print("<p>")
#         print(block)
#         print('</p>')
# print('</body></html>')

handler = HTMLRenderer()
print(handler.sub('emphasis'))
print(re.sub(r'\*(.+?)\*',handler.sub('emphasis'),'This *is* a test'))
