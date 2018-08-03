# -*- coding: utf-8 -*-
# @Date:2018-08-02 23:39:47
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-02 23:53:59
import requests
import json
import pandas
import csv
import io
import sys
import re
import codecs
import time
from pyquery import PyQuery as pq
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


def www_zhihu_com_explore():
    url = 'https://www.zhihu.com/explore'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 1 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    doc = pq(html)
    items = doc('.explore-tab .feed-item').items()
    for item in items:
        question = item.find('h2').find('a').text()
        author = item.find('.author-link-line').text()
        answer = pq(item.find('.content').html()).text()
        myfile = codecs.open('explore.txt', 'a', encoding='utf-8')
        myfile.write('\n'.join([question, author, answer]))
        myfile.write('\n'+"="*50+"\n")
        myfile.close()


def json_modle():
    data = [{
        "name": "何睿",
        "gender": "男",
        'birthday': '1997.04.03'
    }]
    with codecs.open('temp.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def csv_modle():
    with codecs.open('temp.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['id', 'name', 'age'])
        writer.writerows([['10001', 'Mike', '20'], [
                         '10002', 'Bob', '21'], ['10003', 'Jordan', '22']])

    with codecs.open('temp.csv', 'w', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'age']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"id": "1", "name": "何睿", "age": "20"})
        writer.writerow({"id": "2", "name": "李玉", "age": "21"})
        writer.writerow({"id": "3", "name": "王刚", "age": "27"})

    with codecs.open('temp.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

    df = pandas.read_csv('temp.csv')
    print(df)


if __name__ == "__main__":
    pass
