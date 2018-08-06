# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-05 21:21:45
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-06 15:09:51

import urllib
import requests
import json
import openpyxl
import os
import re
import glob
from math import sqrt

# =============参数练习=============


def story(**kwds):
    return "Once upon a time there was a "\
        "%(job)s called %(name)s." % kwds


def power(x, y, *others):
    if others:
        print("Recived redundant parameters:", others)
    return pow(x, y)


def interval(start, stop=None, step=1):
    'Imitates range() for step >0'
    if stop is None:
        start, stop = 0, start
    result = []
    i = start
    while i < stop:
        result.append(i)
        i += step
    return result


def param_driver():
    print(story(job='king',name='Gumby'))
    print(story(name='Sir Robin',job='brave knight'))
    params = {'job':'language','name':'Python'}
    print(story(**params))
    del params['job']
    print(story(job='stoke of genius',**params))
    print(power(2,3))
    print(power(3,2))
    power(x=2,y=3)
    params =(5,)*2
    print(power(*params))
    print(power(3,3,'Hello,world'))
    print(interval(10))
    print(interval(3,12,4))
    print(power(*interval(3,7)))

def multiplier(factor):
    print('factor:',factor)
    def mutiplyByFactor(number):
        print('number:',number)
        return factor*number
    return mutiplyByFactor
double = multiplier(2)
double(5)

if __name__ == "__main__":
    param_driver()
