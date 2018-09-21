# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-04 13:13:47
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-04 15:08:30
import requests
import json
import io
import os
import csv
import sys
import re
import codecs
import time
import pymysql
import pandas
from hashlib import md5
from bson.objectid import ObjectId
from pymongo import MongoClient
from pyquery import PyQuery as pq
from urllib.parse import urlencode
from multiprocessing.pool import Pool
from redis import StrictRedis, ConnectionPool
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


def write_json(json_content, path='temp.json'):
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_content, ensure_ascii=False))


def get_page(offset):
    base_url = "https://www.toutiao.com/search_content/?"
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
    }
    url = base_url+urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            write_json(response.json())
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None


def get_images(json_content):
    data = json_content.get('data')
    if data:
        for item in data:
            title = item.get('title')
            images = item.get('image_list')
            try:
                for image in images:
                    yield{
                        'image': "http:"+image.get('url'),
                        'title': re.sub(r'[\/\\\:\*\?\"\<\>\|]', '', title)
                    }
            except Exception as e:
                print(e.args)


def save_image(item, base_path=r'C:\HeRui\Temp\Download',large=True):
    title = item.get('title')
    image_url = item.get('image')
    if large:
        image_url = re.sub('list','large',image_url)
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    if title and image_url:
        path = os.path.join(base_path, title)
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                file_path = "{0}/{1}.{2}".format(path,
                                                 md5(response.content).hexdigest(), 'jpg')
                if not os.path.exists(file_path):
                    with codecs.open(file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print("Already Download", file_path)
        except requests.ConnectionError as e:
            print("Failed to save image", e.args)


def driver(offset):
    json_content = get_page(offset)
    for item in get_images(json_content):
        save_image(item)


if __name__ == "__main__":
    group_start = 1
    group_end = 20
    pool = Pool()
    groups = [x*20 for x in range(group_start, group_end+1)]
    pool.map(driver, groups)
    pool.close()
    pool.join()
