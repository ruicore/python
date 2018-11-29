# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-11-29 19:38:10
# @Last Modified by:   何睿
# @Last Modified time: 2018-11-29 20:08:12

from collections import namedtuple

# 方式一
NAME, AGE, SEX, EMAIL = range(4)
sutdent = ("Mary", 18, "female", '765809435@qq.com')
print("方式一", sutdent[NAME], sutdent[AGE], sutdent[SEX], sutdent[EMAIL])

# 方式二
Student = namedtuple('Student', ["name", 'age', 'sex', 'email'])
s1 = Student("Mary", 18, "female", '765809435@qq.com')
s2 = Student(name="Harry", age=28, sex="male", email='778809435@qq.com')
print(isinstance(s1,tuple))
print("方式二", s2)
