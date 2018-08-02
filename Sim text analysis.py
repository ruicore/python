# -*- coding: utf-8 -*-
# @Date:   2018-08-02 12:39:11
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-02 12:49:26

import urllib
import requests
import json
import openpyxl
import os
import re
import glob


def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=CNLZcnqL3E6NLeFNGzUE06fY&client_secret=b8Z7nQPmASHHhPLjRG6dXKQG7W97DxNk'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    content = json.loads(content)
    if content:
        return content["access_token"]


'''接口接入，返回json格式数据'''


def get_content(data):
    access_token = get_access_token().strip()
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?access_token=" + \
        access_token  # API
    headers = {"Content-Type":"application/json"}
    try:
        data = json.dumps(data)
        r = requests.post(url, data=data, headers=headers)
        return r.text
    except Exception as e:
        print(e)
        return 0

def analysis(path):
    work_book= openpyxl.load_workbook(path)
    sheet = work_book[work_book.sheetnames[0]]
    data = {"text_1": "","text_2":""}
    for row in sheet.rows:
        data["text_1"] = row[0].value
        data["text_2"] = row[1].value
        print(json.loads(get_content(data))["score"])

if __name__=="__main__":
    analysis(r'C:\HeRui\Tim\词义相似度.xlsx')