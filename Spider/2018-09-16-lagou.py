# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-16 16:41:20
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-16 17:00:25

import codecs
import time
import json
from urllib import request, parse


def lagou(pages=30):

    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    data = {
        "first": "false",
        "pn": 1,
        'kd': "python"
    }
    headers = {
        'Cookie': "_ga=GA1.2.562214235.1536581221; user_trace_token=20180910200700-05abf0b8-b4f2-11e8-b62b-5254005c3644; LGUID=20180910200700-05abf414-b4f2-11e8-b62b-5254005c3644; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAAAIAACBIE966AF6F31795B53E22AFC8D107BB51D; LGSID=20180916154940-114dbf9c-b985-11e8-bad0-5254005c3644; _gid=GA1.2.1154832757.1537084179; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536581221,1537084179; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537087506; LGRID=20180916164507-d079c6b4-b98c-11e8-bad0-5254005c3644; TG-TRACK-CODE=search_code; SEARCH_ID=eaff8aa90267410296f394f13f68dc18",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
        "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    }
    for page in range(pages):
        data['pn'] = page+1
        data_ = parse.urlencode(data).encode('utf-8')
        req = request.Request(url=url, data=data_, headers=headers)
        resp = request.urlopen(req)
        with codecs.open('temp//'+'secret'+str(page+1)+'.json', 'w', 'utf-8') as f:
            f.write(resp.read().decode('utf-8'))


if __name__ == "__main__":
    lagou(30)
