# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-12 19:38:56
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-12 19:39:06


def lines(_file):
    for line in _file:
        yield line
    yield '\n'


def blocks(_file):
    block = []
    for line in lines(_file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block=[]
