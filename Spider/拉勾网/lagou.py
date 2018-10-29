# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-09-16 16:41:20
# @Last Modified by:   何睿
# @Last Modified time: 2018-09-16 17:00:25

import sys
sys.path.append('..')
import math
import codecs
import random
import time
import json
import requests
import pandas as pd
from ips import proxies


def get_json(kind, page=1,):
    # kind 搜索关键字
    # page 页码
    param = {
        'first': "false",
        'pn': page,
        'kd': kind
    }
    headers = {
        "Host": 'WWW.lagou.com',
        "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    # 请求的url
    url = "https://www.lagou.com/jobs/positionAjax.json?city=%E6%AD%A6%E6%B1%89&needAddtionalResult=false"
    response = requests.post(url, headers=headers, data=param, proxies={
                             "http": random.choices(proxies)})
    response.encoding = 'utf-8'
    if response.status_code == 200:
        response = response.json()
        try:
            return response['content']['positionResult']
        except Exception as e:
            print(e.args)
            return None
    return None


def drive():
    # 默认先爬取第一页的数据
    kind = "python"
    # 请求一次 获取总条数
    position_result = get_json(kind=kind)
    # 总条数
    total = position_result.get("totalCount", -1)
    print("{}开发职位，招聘信息总共{}条......".format(kind, total))
    # 每页15条 向上取整 算出总页数
    page_total = math.ceil(total/15)

    # 所有的查询结果
    search_job_result = []
    for i in range(1, page_total+1):
        position_result = get_json(kind=kind, page=i)
        if not position_result:
            continue
        #  每次抓取完成之后，暂停一会，防止爬虫被禁止
        time.sleep(15)
        page_job = []
        for j in position_result.get("result"):
            job = []
            # 公司全名
            job.append(j.get("companyFullName", "Not Found"))
            # 公司简称
            job.append(j.get('companyShortName', "Not Found"))
            # 公司规模
            job.append(j.get('companySize', "Not Found"))
            # 融资
            job.append(j.get('financeStage', "Not Found"))
            # 所属区域
            job.append(j.get('district', "Not Found"))
            # 职称
            job.append(j.get('positionName', "Not Found"))
            # 要求工作年限
            job.append(j.get('workYear', "Not Found"))
            # 招聘学历
            job.append(j.get('education', "Not Found"))
            # 薪资范围
            job.append(j.get('salary', "Not Found"))
            # 福利待遇
            job.append(j.get('positionAdvantage', "Not Found"))
            page_job.append(job)
        # 放入所有的列表中
        search_job_result += page_job
        print('第{}页数据爬取完毕, 目前职位总数:{}'.format(i, len(search_job_result)))
    # 将总数据转化为data frame再输出
    df = pd.DataFrame(data=search_job_result,
                      columns=['公司全名', '公司简称', '公司规模', '融资阶段', '区域', '职位名称', '工作经验', '学历要求', '工资', '职位福利'])
    df.to_csv('lagou.csv', index=False, encoding='utf-8_sig')


def analysis():
    # 读取数据
    df = pd.read_csv('lagou.csv', encoding='utf-8_sig')
    df.drop(df[df['职位名称'].str.contains("实习")].index,inplace=True)
    # 由于csv文件内的数据是字符串形式，先用正则表达式将字符串转化为列表，再取区间的均值
    pattern = r"\d+"
    df['work_year'] = df["工作经验"].str.findall(pattern)
    avg_work_year = []
    for i in df["work_year"]:
        #如果工作经验为"不限"或者为"应届毕业生",那么匹配值为空，工作年限为0
        if len(i) == 0:
            avg_work_year.append(0)
        # 如果匹配值为一个数值，那么返回该值
        elif len(i)==1:
            avg_work_year.append(int(''.join(i)))
        else:
            num_list = [int(j) for j in i]
            avg_year = sum(num_list)/2
            avg_work_year.append(avg_year)
    df["工作经验"] = avg_work_year
    # 将字符串转化为列表，再取区间的前25%，比较贴近现实
    df['salary'] = df["工资"].str.findall(pattern)
    # 月薪
    avg_salary = []
    for k in df["salary"]:


if __name__ == "__main__":
    analysis()
