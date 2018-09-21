# -*- coding: utf-8 -*-
# @Author:             何睿
# @Last Modified time: 2018-09-21 18:21:56
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-21 21:31:01

import re


def process(text, width):
    if not 10 <= width <= 80:
        print("ERROR: Width out of range!")
    error_test = '[A-Za-z ]*'
    error_patrn = re.compile(error_test)
    res = error_patrn.match(text)
    length = len(text)
    span = res.span()
    result = ""
    if span[1]-span[0] == length:
        pattern = re.compile("[A-Za-z]+")
        index = []
        for item in pattern.finditer(text):
            index.extend([item.span()[0], item.span()[1]])
        if index[0]:
            index.insert(0, 0)
        if not index[-1] == length:
            index.append(length)
        for i in range(len(index)-1):
            j = i+1
            result += text[index[i]:index[j]]
            before, after = index[i] // width+1, index[j] // width+1
            if after-before:
                result += "(%s,%s)%s" % (str(before), str(after), ";")
            else:
                result += "(%s)%s" % (str(before), ";")
        print(result)
    else:
        print("ERROR: Invalid character detected!")


if __name__ == "__main__":
    process("The main theme of education in engineering school is learning to teach yourself", 10)
