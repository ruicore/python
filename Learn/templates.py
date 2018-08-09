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


emphasis_pattern = re.compile(r'''
        \*          # Beginning emphasis tag -- an asterisk
        (           # Begin group for capturing phrase
        [^\*]+      # Capture anything except asterisk
        )           # End group
        \*          # Ending emphasis tag
        ''', re.VERBOSE)
print(re.sub(emphasis_pattern,r'<em>\1</em>','Hello,*world*!'))
