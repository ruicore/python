# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-09 14:49:09
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-09 16:27:40

import sys


# sys.setrecursionlimit(100000)
# 二进制转换成为十进制 v = '0b1111011'
print(int('0b1111011', 2))
# 十进制转换成为二进制 v = '28'
print(bin(18))
# 八进制转换成为十进制 v = '011'
print(int('011', 8))
# 十进制转换成为八进制 v = '30'
print(oct(30))
# 十六进制转换成为十进制 v = '0x12'
print(int('0x12', 16))


def fab(n):
    # python 最大的递归层数
    if n == 1:
        return 1
    else:
        return fab(n - 1) + n


# 三元运算符
# 为真时的结果 if 判定条件 else 为假时候的结果
1 if 3 > 2 else 0
# 用一行代码实现数值交换
a = 1
b = 2
a, b = b, a

if __name__ == "__main__":
    print(fab(999))
