# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-10 10:07:36
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-10 10:09:29

# 01====变量交换====
# Bad
a = 0
b = 1
temp = a
a = b
b = temp
# Pythonic
a, b = b, a
# 02===列表推导===
my_list = []
# Bad
for i in range(10):
    my_list.append(i*2)
# pythonic
my_list = [i*2 for i in range(10)]
# 03单行表达式
# 带索引遍历
# Bad
for i in range(len(my_list)):
    print(i, '--->', my_list[i])
# pythonic
for i, item in enumerate(my_list):
    print(i, '-->', item)
# 05序列解包
a, *test = [1, 2, 3]
a, *middle, c = [1, 2, 3, 4]
# 06 字符串拼接
# Bad
letters = ['s', 'p', 'a', 'm']
s = ''
for let in letters:
    s += let
# pythonic
word = ''.join(letters)
# 07 真假判断
attr = True
# bad
if attr == True:
    print("Ture")
if attr == False:
    print("False")
# pythonic
if attr:
    print("Ture")
if not attr:
    print("False")
# 08 访问字典元素
d = {'hello': 'world'}
print(d.get('hello', 'default_value'))
# 09 操作列表
a = [3, 4, 5]
b = []
# Bad
for i in a:
    if a > 4:
        b.append(i)
# pythonic
b = [i for i in a if i > 4]
b = filter(lambda x: x > 4, a)
a = [3, 4, 5]
# bad
for i in range(len(a)):
    a[i] += 3
# pythonic
a = [i+3 for i in a]
a = map(lambda i: i+3, a)
# 14 链式比较
age = 60
# bad
if age > 18 and age < 60:
    print('young man')
# pythonic:
if 18 < age < 60:
    print("young man")
    
