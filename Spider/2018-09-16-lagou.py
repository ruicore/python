# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-16 16:42:52
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-16 16:42:52

import codecs
import time
from urllib import request, parse


def lagou(pages=30):

    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    data = {
        "first": "false",
        "pn": 1,
        'kd': "python"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
        "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    }
    for page in range(pages):
        time.sleep(5)
        data['pn'] = page+1
        data_ = parse.urlencode(data).encode('utf-8')
        req = request.Request(url=url, data=data_, headers=headers)
        resp = request.urlopen(req)
        with codecs.open('temp'+str(page+1)+'.json', 'w', 'utf-8') as f:
            f.write(resp.read().decode('utf-8'))


if __name__ == "__main__":
    lagou(30)
