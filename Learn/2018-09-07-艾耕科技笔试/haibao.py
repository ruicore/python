# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-20 10:29:13
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-20 12:49:33

import os
import sys
import json
import codecs
import pyquery
import hashlib
from pprint import pprint
from urllib import request, parse


def haibao():
    url = 'http://pic.haibao.com/ajax/image:getHotImageList.json?stamp=Thu%20Sep%2020%202018%2010:38:03%20GMT+0800%20(China%20Standard%20Time)'
    headers = {
        "Cookie": "hbUnregUserId=3BEAE823-A6A8-43DD-A3BC-553C6C7D5722; Hm_lvt_9448a813e61ee0a7a19c41713774f842=1537187141,1537410547; Hm_lvt_06ffaa048d29179add59c40fd5ca41f0=1537187141,1537410547; Hm_lvt_793a7d1dd685f0ec4bd2b50e47f13a15=1537187141,1537410547; Hm_lpvt_06ffaa048d29179add59c40fd5ca41f0=1537411022; Hm_lpvt_9448a813e61ee0a7a19c41713774f842=1537411022; Hm_lpvt_793a7d1dd685f0ec4bd2b50e47f13a15=1537411022",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Referer": "http://pic.haibao.com/hotimage/"
    }
    data = {
        "skip": 54
    }
    base_dir = sys.path[0]
    image_dir = os.path.join(base_dir, 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    max_pic = 10000
    pic_num = 0
    has_more = True
    hash_name = hashlib.md5()
    while has_more:
        data_ = parse.urlencode(data).encode("utf-8")
        req = request.Request(url=url, headers=headers, data=data_)
        content = json.loads(request.urlopen(req).read().decode('utf-8'))
        html = content.get("result").get("html")
        doc = pyquery.PyQuery(html)
        img_urls = [img.attr("data-original") for img in doc("img").items()]
        for img_url in img_urls:
            pic_num += 1
            try:
                img_req = request.Request(url=img_url, headers=headers)
                image = request.urlopen(img_req)
                binary_img = image.read()
                hash_name.update(binary_img)
                name = hash_name.hexdigest()
                with open(os.path.join(image_dir, str(name)+".jpg"), 'wb') as f:
                    f.write(binary_img)
            except Exception as e:
                pprint(e)
        skip = content.get("result").get('skip')
        pic_num += skip
        data.setdefault('skip', skip)
        if not content.get("result").get("hasMore") == 1 or pic_num > max_pic:
            has_more = False


if __name__ == "__main__":
    haibao()
