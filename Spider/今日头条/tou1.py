# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-11-10 20:34:20
# @Last Modified by:   何睿
# @Last Modified time: 2018-11-11 12:33:25

import requests
import os
import sys

path_a = os.path.abspath('.')
path_a = os.path.join(path_a,'img')
if not os.path.exists(path_a):
    os.makedirs(path_a)
os.chdir(path_a)

kw = ''
while True:
    kw = input('请输入你要获取的图片(若想结束请输入1)')
    if kw == '1':
        print("已退出，你下载的图片已保存在"+path_a+",请查看")
        break
    for x in range(0,1000,20):
        url = 'https://www.toutiao.com/search_content/?offset='+str(x)+'&format=json&keyword=%s&autoload=true&count=20&cur_tab=3&from=gallery' % kw
        response = requests.get(url)
        data = response.json()['data']
        if not data:
            print("下载"+kw+"图片完毕，请换个关键词继续")
            break
        n = 1 # 记录文章数目
        for atlas in data:
            title = atlas.get('title',"Not Found")
            try:
                if title not in os.listdir(path_a):
                    os.mkdir(title)
            except OSError as e:
                print('文件名出错，创建目录失败，重新创建一个随机名字')
                title = kw + '文件名出错'+str(x)
                if title not in os.listdir(path_a):
                    os.mkdir(title)
            k = 1
            path = os.path.join(path_a,title)
            os.chdir(path)
            try:
                for image in atlas['image_list']:  # 这个链接获取的图片是小张的，换成大的图片
                    image_url = image['url'].replace('list', 'large')  # 改个链接获取大的图片
                    atlas = requests.get('http:'+image_url).content
                    with open(str(k)+'.jpg', 'wb') as f:  # 把图片写入文件内
                        f.write(atlas)
                    print('下载完第%d个文章的%d幅图完成：%s' % (x+n, k,image_url))
                    k += 1
            except Exception as e:
                print(e.args)
            n += 1
            # 转出图片目录
            os.chdir(path_a)
