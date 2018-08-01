# -*- coding: utf-8 -*-
# @Date 2018-08-01 16:04:48
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-01 16:09:17
# Date time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(r"C:\Git\Python\Spider\maoyan-com-board-4.py"))
# Last Modified time:  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

import json
import requests
import re
import time
import codecs
import os
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 1 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else "",
            'time': item[4].strip()[5:] if len(item[4]) > 5 else "",
            'score': item[5].strip()+item[6].strip()
        }


def write_to_file(content):
    with codecs.open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(offset):
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == "__main__":
    if os.path.exists('result.txt'):
        os.remove('result.txt')
        print("存在同名文件，将删除原文件，重新创建新文件")
        time.sleep(3)
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
