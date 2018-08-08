# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-07 11:49:46
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-08 10:58:04

import sys
import string
from math import pi
from pprint import pprint
from string import Template


_format_1 = 'Hello,%s.%s enough for you'
values = ('world', 'Hot')
pprint(_format_1 % values)
_format_2 = 'Pi with three decimal:%.3f'
pprint(_format_2 % pi)

s_1 = Template("$x, glorious $x $$")
result_1 = s_1.safe_substitute(x='slurm')
pprint(result_1)

s_2 = Template("It's ${x}tastic!")
result_2 = s_2.safe_substitute(x="slurm")
pprint(result_2)

s_3 = Template('A $thing must never $action')
d = {}
d['thing'] = 'gentleman'
d['action'] = 'show his socks'
result_3 = s_3.safe_substitute(d)
pprint(result_3)

s_4 = "%s plus %s equals %s " % (1, 2, 3)
pprint(s_4)

s_5 = 'Price of eggs:%d' % (42)
s_6 = 'Hexadecimal price of eggs: %x' % 42
s_7 = 'Pi:%f...' % pi
s_8 = "Very inexact estimate of pi:%i" % pi
s_9 = "Using str:%s" % 42
pprint(s_5)
pprint(s_6)
pprint(s_7)
pprint(s_8)
pprint(s_9)

s_10 = "%10f" % pi
s_11 = "%10.2f" % pi
s_12 = "%.2f" % pi
print(s_10)
pprint(s_11)
pprint(s_12)

# 0 表示将会用数字“0”进行填充
s_13 = "%010.2f" % pi
pprint(s_13)
# - 用于左对齐
s_14 = '%-10.2f ' % pi
# " "用于在正数前面加上空格
s_15 = '% 5d' % 10+"\r\n"+"% 5d" % -10
pprint(s_14)
print(s_15)
# "+" 不管是正数还是负数前面都出现符号
s_16 = '%+5d' % 10+"\r\n"+"%+5d" % -10
print(s_16)

width = 35
price_width = 10
item_with = width-price_width
header_format = "%-*s%*s"
_format = "%-*s%*.2f"
pprint("="*width)
pprint(header_format % (item_with, "item", price_width, "price"))
pprint("-"*width)
pprint(_format % (item_with, 'Apples', price_width, 0.4))
pprint(_format % (item_with, "Pears", price_width, 0.5))
pprint(_format % (item_with, 'Cantaloupes', price_width, 1.92))
pprint(_format % (item_with, "Dried Apricots(16 oz.)", price_width, 8))

s_18 = "with a moo-moo here. and a moo-moo there".find("moo")
print(s_18)
subject = "$$$ Get rich now!!! $$$"
result = subject.find("$$$",0,16)
print(result)

seq = [1,2,3,4,5,6]
sep ="+"
result = sep.join(str(x) for x in seq)
print(result)

dirs = '','usr','bin','env'
print("/".join(dirs))

s_19 = "that's all folks".title()
s_20= string.capwords("that's all folks")
print(s_19)
print(s_20)

s_21 = "This is a test".replace('is','ezz')
print(s_21)

s_22 = "***SPAM * for *everyone!!! ***".strip(" *")
pprint(s_22)

table = str.maketrans('cs','kz')
s_23 = "this is an incredible test".translate(table)
pprint(s_23)