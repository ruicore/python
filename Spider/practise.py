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
import pymysql
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

def mysql():
    db = pymysql.connect(host='localhost', user='root',password="#FcUO%nj9FKrVa2&^AFW", port=3306, db='spiders')
    data = {'id': 2007,'name': "李玉",'age': 27}
    table = 'students'
    keys = ', '.join(data.keys())
    values = ', '.join(["%s"]*len(data))
    cursor = db.cursor()

    # insert
    sql_insert = 'INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql_insert, tuple(data.values())):
            print("Sucessful")
            db.commit()
    except:
        print('failed')
        db.rollback()
    db.close()

    sql_update = "UPDATE students SET age = %s WHERE name = %s"
    try:
        cursor.execute(sql_update, (25, "何睿"))
        db.commit()
    except:
        db.rollback()
    db.close()

    sql_insert_with_no_duplicate = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table,keys=keys, values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql_insert_with_no_duplicate +=update
    try:
        if cursor.execute(sql_insert_with_no_duplicate,tuple(data.values())*2):
            print("Sucessful")
            db.commit()
    except:
        print("Failed")
        db.rollback()
    print(sql_insert_with_no_duplicate)

    condition = 'age > 20'
    sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table,condition=condition)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

    sql = 'SELECT * FROM students WHERE age > 20'
    try:
        # fetchone 使得指针偏移，fetchall可能不会打印所有的数据
        cursor.execute(sql)
        print('Count:',cursor.rowcount)
        one = cursor.fetchone()
        print('one:',one)
        results = cursor.fetchall()
        print("Results:",results)
        print("Results Type",type(results))
        for row in results:
            print(row)
        row = cursor.fetchone()
        while row:
            print("Row:",row)
            row = cursor.fetchone()
    except:
        print("Error")


if __name__ == "__main__":
    pass
