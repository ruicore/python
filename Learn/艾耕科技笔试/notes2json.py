# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-19 19:56:07
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-19 19:58:02

import re
import os
import time
import json
import codecs
from pprint import pprint


def set_key(node_dict, keys, values):
    try:
        temp_list = node_dict[keys[0]]
    except:
        pprint("根节点未找到")
        return -1
    for key in keys[1:]:
        for sub_dict in temp_list:
            temp_list = sub_dict.get(key)
            if isinstance(temp_list, list):
                break
    for value in values:
        temp_dict = {value: []}
        if not temp_dict in temp_list:
            temp_list.append(temp_dict)
            temp_list = temp_dict.get(value)
    return


def notes2json(content_path, write_path):
    # 字符串匹配，匹配字符串前面的逗号
    pattern = re.compile('^,+')
    lines = [line.strip() for line in codecs.open(
        content_path, 'r', 'utf-8').readlines()]
    lines[0] = lines[0].split(',')
    lines[0].insert(0, 0)
    # 统计每一行前面的逗号，以逗号分隔每一行
    for index in range(1, len(lines)):
        span = pattern.match(lines[index]).span()
        num = span[1]-span[0]
        lines[index] = re.sub(pattern, '', lines[index])
        lines[index] = lines[index].split(',')
        lines[index].insert(0, num)
    # 初始化根节点
    master_key = lines[0][1]
    if master_key:
        node_dict = {master_key: []}
    else:
        pprint("根不存在，请重新输入")
    master = node_dict[master_key]
    for key in lines[0][2:]:
        master.append({key: []})
        master = master[0].get(key)
    # 给每一行找到合适的位置
    for index, line in enumerate(lines[1:]):
        num = line[0]
        # 找到line上层的所有键
        j = index
        keys = []
        while j >= 0:
            while num <= lines[j][0]:
                j -= 1
            try:
                for i in range(num-lines[j][0], 0, -1):
                    keys.insert(0, lines[j][i])
            except:
                pprint("该层的直接上一层不能提供足够的节点，将使用上一层的所有节点作为父节点")
                length = len(lines[j])
                for i in range(length-1, 0, -1):
                    keys.insert(0, lines[j][i])
            num = lines[j][0]
            j -= 1
        set_key(node_dict, keys, line[1:])
    with codecs.open(write_path, 'w', 'utf-8') as f:
        f.write(json.dumps(node_dict, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    base_path = os.path.abspath('.')
    content_path = os.path.join(base_path, "concepts.txt")
    write_path = os.path.join(base_path, 'result.json')
    notes2json(content_path, write_path)
