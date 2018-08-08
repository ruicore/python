# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-06 19:21:13
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-05 21:08:40

import sys
import os
import webbrowser
import fileinput
from pprint import pprint
from collections import deque
from heapq import *
from random import shuffle
from functools import reduce

# pprint(os.linesep)
# webbrowser.open('www.baidu.com')
# os.system(r'"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"') # 11
# os.startfile(r'"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"') # 12

# for line in fileinput.input(inplace=True):
#     line = line.rstrip(" \r\n")
#     num = fileinput.filelineno()
#     print("%-40s # %2i" % (line, num))

# myset = set([1, 2, 4, 5, 7, 8, 4, 5, 6, 5])
# a = set([1, 2, 3])
# b = set([2, 3, 4])
# uni = a.union(b)
# c = a & b
# pprint(c.issubset(a))
# pprint(uni)
# pprint(c.issubset(b))
# pprint(c >= a)
# pprint(a.intersection(b))
# pprint(a.difference(b))
# pprint(a-b)
# pprint(a.symmetric_difference(b))
# pprint(a ^ b)
# pprint(a.copy())
# pprint(a.copy() is a)
# mySets = []
# for i in range(10):
#     mySets.append(set(range(i,i+5)))
# pprint(reduce(set.union,mySets))

# data = list(range(10))
# heap =[]
# shuffle(data)
# for n in data:
#     heappush(heap,n)
# heapify(data)
# pprint(heap)
# pprint(data)
# heapreplace(heap,10)
# pprint(heap)

# 双端队列
q = deque(range(5))
q.append(5)
q.appendleft(6)
q.pop()
pprint(q)
q.popleft()
pprint(q)
q.rotate(3)
pprint(q)
q.rotate(-1)
pprint(q)