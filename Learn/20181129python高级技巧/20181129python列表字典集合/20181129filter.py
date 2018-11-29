# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-11-29 17:31:26
# @Last Modified by:   何睿
# @Last Modified time: 2018-11-29 19:24:08

import random
import timeit


# 筛选出列表中的非负数
# 生成15个范围在-20，20之间的整数

data = [random.randint(-20, 20) for _ in range(15)]

# 使用filter函数过滤，并转换为list
res_list_filter = list(filter(lambda x: x >= 0, data))

# 使用列表推导式过滤
res_list_list = [x for x in data if x >= 0]

t1 = timeit.timeit("list(filter(lambda x: x >= 0, data))",
                   setup='data = {0}'.format(data), number=10000)
t2 = timeit.timeit("[x for x in data if x >= 0]",
                   setup='data = {0}'.format(data), number=10000)

# 字典，选出成绩大于等于85的学生
# 生成20个学生的成绩，编号从1到20，作为键；成绩为值，范围60-100
mydict = {k: random.randint(60, 100) for k in range(1, 21)}

res_dict_filter = dict(filter(lambda k: k[1] >= 85, mydict.items()))
res_dict_list = {k: v for k, v in mydict.items() if v >= 85}

# 集合
myset = set(data)
myset_list = {x for x in myset if x >= 0}
myset_filter = set(filter(lambda x: x > 0, myset))

t3 = timeit.timeit("{x for x in myset if x >= 0}", setup="myset = {0}".format(myset))
t4 = timeit.timeit("set(filter(lambda x: x > 0, myset))",
                   setup='myset = {0}'.format(myset))
print(t3, t4)
