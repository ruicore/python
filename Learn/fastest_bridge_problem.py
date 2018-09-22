# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-22 10:43:54
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-22 11:56:47

import random


def bridge(minutes):
    # 人数
    num = len(minutes)
    if num <= 2:
        return [tuple(minutes)], sum(minutes)
    else:
        # 需要的总时间
        times = 0
        result = []
        # 判读是奇数个人还是偶数个人
        is_even = False if num % 2 else True
        i = 2 if is_even else 3
        s_lst = sorted(minutes)
        while i < num:
            if 2*s_lst[1] >= s_lst[0]+s_lst[i]:
                temp = [(s_lst[0], s_lst[i]), (s_lst[0]),(s_lst[0], s_lst[i+1]), (s_lst[0])]
                result.extend(temp)
                times += sum([2*s_lst[0], s_lst[i], s_lst[i+1]])
                del temp
            else:
                temp = [(s_lst[0], s_lst[1]), (s_lst[0]),(s_lst[i], s_lst[i+1]), (s_lst[1])]
                times += sum([2*s_lst[1], s_lst[0], s_lst[i+1]])
                result.extend(temp)
                del temp
            i += 2
        if is_even:
            result.append((s_lst[0], s_lst[1]))
            times += s_lst[1]
        else:
            temp = [(s_lst[0], s_lst[1]), (s_lst[0]), (s_lst[0], s_lst[2])]
            times += sum([s_lst[1], s_lst[2]])
            result.extend(temp)
        return result,times


if __name__ == "__main__":
    # minutes = [1, 2, 5, 10]
    minutes = random.sample(range(1, 100), 10)
    res = bridge(minutes)
    print(res)
