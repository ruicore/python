# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-04 09:13:47
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-04 11:30:15
import requests
import json
import io
import csv
import sys
import re
import codecs
import time
import pymysql
import pandas
from bson.objectid import ObjectId
from pymongo import MongoClient
from pyquery import PyQuery as pq
from urllib.parse import urlencode
from redis import StrictRedis, ConnectionPool
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


base_url = "https://m.weibo.cn/api/container/getIndex?"
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 1 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['weibo']
collection = db['weibo']


def write_json(json_content, path='temp.json'):
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_content, ensure_ascii=False))


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url+urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json_content):
    if json_content:
        items = json_content.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            try:
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get("reposts_count")
                yield weibo
            except Exception as e:
                print(e.args)


def save_to_mongo(result):
    try:
        collection.insert_one(result)
    except Exception as e:
        print(e.args)


if __name__ == "__main__":
    for page in range(1, 11):
        json_content = get_page(page)
        results = parse_page(json_content)
        for result in results:
            save_to_mongo(result)
