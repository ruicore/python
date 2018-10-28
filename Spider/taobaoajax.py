# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-19 09:48:50
# @Last Modified by:   何睿
# @Last Modified time: 2018-10-28 14:58:48

import openpyxl
import requests
import json
import csv
import time
from pprint import pprint


class TaoBao():
    def __init__(self):
        self.auctions_distinct = []
        # url = 'https://s.taobao.com/api?callback=jsonp227&m=customized&q=%s&s=%s' % (k, p)
        self.keys = ['Iphone', 'Python']
        self.max_page = 100
        self.json_key = "jsonp280"
        self.url = "https://s.taobao.com/api?_ksTS=1540273014777_279&callback=%s&ajax=true&m=customized&stats_click=search_radio_all:1&q=%s&s=%s&imgfile=&initiative_id=staobaoz_20181023&bcoffset=-1&js=1&style=grid&ie=utf8&rn=2d60b78e90963e4e9fc4d50dff6e8cdb"
        self.headers = {
            "Referer": "https://s.taobao.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "content-type": "application/json;charset=UTF-8",
            "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

    def write_excel(self, response_auctions_info, file_name):
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = str(file_name.split('.')[0])
        ws1.append(['标题', '价格', '销量', '店铺', '区域', '图片'])
        for i in response_auctions_info:
            raw_title = str(i.get("raw_title"))
            if raw_title not in self.auctions_distinct:
                view_price = i.get('view_price', "Not Found")
                view_sales = i.get('view_sales', "Not Found")
                nick = i.get('nick', "Not Found")
                item_loc = i.get('item_loc', "Not Found")
                pic_url = i.get('pic_url', "Not Found")
                row = [raw_title, view_price,
                       view_sales, nick, item_loc, pic_url]
                ws1.append(row)
                self.auctions_distinct.append(raw_title)
        wb.save(file_name)

    def crawl(self,):
        for key in self.keys:
            file_name = "{0}.xlsx".format(key)
            response_auctions_info = []
            for page in range(self.max_page):
                json_key = "jsonp280"
                url = self.url % (json_key, key, page)
                r = requests.get(url, timeout=30, headers=self.headers)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                time.sleep(3)
                response = r.text
                response = response.strip().split(
                    json_key+"(")[1].split(");")[0]
                response_dict = json.loads(response)
                auctions = response_dict['API.CustomizedApi']['itemlist']['auctions']
                response_auctions_info += auctions
                print("第%d个页面，共%d个宝贝" % ((page+1), len(auctions)))
            self.write_excel(response_auctions_info, file_name)
            print('%s共爬取到%d个宝贝长度'%(key,len(self.auctions_distinct)))


if __name__ == '__main__':
    taobao = TaoBao()
    taobao.crawl()
