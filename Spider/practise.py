# -*- coding: utf-8 -*-
# @Date:2018-08-02 23:39:47
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-02 23:53:59
import requests
import json
import io
import sys
import re
import codecs
import time
from pyquery import PyQuery as pq
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


def www_zhihu_com_explore():
    url = 'https://www.zhihu.com/explore'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 1 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    html = requests.get(url,headers=headers).text
    doc = pq(html)
    items = doc('.explore-tab .feed-item').items()
    for item in items:
        question = item.find('h2').find('a').text()
        author = item.find('.author-link-line').text()
        answer = pq(item.find('.content').html()).text()
        myfile = codecs.open('explore.txt','a',encoding='utf-8')
        myfile.write('\n'.join([question,author,answer]))
        myfile.write('\n'+"="*50+"\n")
        myfile.close()

def json_modle():
    data=[{
    "name":"何睿",
    "gender":"男",
    'birthday':'1997.04.03'
    }]
    with codecs.open('temp.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data,indent=4,ensure_ascii=False))

if __name__=="__main__":
    pass