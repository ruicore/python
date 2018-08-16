# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-16 09:51:38
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-16 10:29:16

from nntplib import NNTP
from time import strftime, time, localtime
from email import message_from_string
from urllib.request import urlopen
import textwrap
import re

day = 24*60*60  # 一天的秒数


def wrap(string, max=70):
    """
    将字符串调整为最大行宽
    """
    return "\n".join(textwrap.wrap(string))+"\n"


class NewsAgent:
    """
    可以从新闻来源获取新闻项目并且发布到新闻目标的对象
    """

    def __init__(self):
        self.sources = []
        self.destinations = []

    def addSource(self, source):
        self.sources.append(source)

    def addDestination(self, dest):
        self.destinations.append(dest)

    def distribute(self):
        """
        从所有来源获取所有新闻项目并且发布到所有目标
        """
        items = []
        for source in self.sources:
            items.extend(source.getItems())
        for dest in self.destinations:
            dest.receiveItems(items)


class NewsItem:
    """
    包括标题和主体文本的简单新闻项目
    """

    def __init__(self, title, body):
        self.title = title
        self.body = body


class NNTPSource:
    """
    从NNTP组中获取新闻项目的新闻来源
    """

    def __init__(self, servername, group, window):
        self.servername = servername
        self.group = group
        self.window = window

    def getItems(self):
        start = localtime(time()-self.window*day)
        date = strftime("%y%m%d", start)
        hour = strftime("%H%M%S", start)
        server = NNTP(self.servername)
        ids = server.newnews(self.group, date, hour)[1]
        for id in ids:
            lines = server.article(id)[3]
            message = message_from_string("\n".join(lines))

            title = message['subject']
            body = message.get_payload()
            if message.is_multipart():
                body = body[0]
            yield NewsItem(title, body)
        server.quit()


class SimpleWebSource():
    """
    使用正则表达式从网页中提取新闻项目的新闻来源
    """

    def __init__(self, url, titlePattern, bodyPattern):
        self.url = url
        self.titlePattern = titlePattern
        self.bodyPattern = bodyPattern

    def getItems(self):
        text = urlopen(self.url).read()
        titles = self.titlePattern.findall(text)
        bodies = self.bodyPattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, wrap(body))


class PlainDestination:
    """
    将所有新闻项目格式化为HTML的目标类
    """

    def receiveItems(self, items):
        for item in items:
            print(item.title)
            print('-'*len(item.title))
            print(item.body)


class HTMLDestination:
    """
    将所有新闻项目格式化为HTML的目标类
    """

    def __init__(self, filename):
        self.filename = filename

    def receiveItems(self, items):
        out = open(self.filename, 'w')
        print("""
        <html>
            <head>
            <title>Today's News</title>
            </head>
            <body>
            <h1>Today's News<h1>
            """,
              file=out)
        print("<ul>", file=out)
        _id = 0
        for item in items:
            _id += 1
            print('<h2><a name ="%i">%s</a></h2>' %
                  (_id, item.title), file=out)
        print('</ul>', file=out)
        _id = 0
        for item in items:
            _id += 1
            print('<h2><a name="%i">%s</a></h2>' % (_id, item.title), file=out)
            print('<pre>%s</pre>' % item.body, file=out)
        print("""
        </body>
        </html>
        """, file=out)
    def runDefaultSetup():
        """
        来源和目标的默认设置。可以自己修改
        """
        agent = NewsAgent()
        # 从BBS新闻站获取新闻的SimpleWebSource
        bbc_url = 