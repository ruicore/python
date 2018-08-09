# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-09 11:05:17
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-09 11:34:36
# python .\templates.py .\magnus.txt .\template.txt

import fileinput
import re

filed_part = re.compile(r'\[(.+?)\]')
scope = {}


def replacement(match):
    # 用于re.sub中
    code = match.group(1)
    try:
        return str(eval(code, scope))
    except SyntaxError:
        exec(code, scope)
        return ''


lines = []
for line in fileinput.input():
    lines.append(line)
text = ''.join(lines)

print(filed_part.sub(replacement, text))
