# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-13 11:27:46
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-13 14:37:36

import sys
import re
from handlers import *
from util import *
from rules import *


class Parser:
    """
    语法分析器读取文本文件，应用规则并且控制处理程序
    """

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.fitlers = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def fitler(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.fitlers.append(filter)

    def parse(self, _file):
        self.handler.start("document")
        for block in blocks(_file):
            block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    在构造函数中增加规则和过滤器的具体语法分析器
    """

    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagrapheRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)
