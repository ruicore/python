# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-14 09:49:36
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-14 10:00:20


from xml.sax.handler import ContentHandler
from xml.sax import parse


class HeadlineHandler(ContentHandler):
    in_headline = False

    def __init__(self, headlines):
        ContentHandler.__init__(self)
        self.headlines = headlines
        self.data = []

    def startElement(self, name, attrs):
        if name == 'h1':
            self.in_headline = True

    def endElement(self, name):
        if name == 'h1':
            text = ''.join(self.data)
            self.data = []
            self.headlines.append(text)
            self.in_headline = False

    def characters(self, string):
        if self.in_headline:
            self.data.append(string)


class PageMaker(ContentHandler):
    passthrongh = False

    def startElement(self, name, attrs):
        if name == 'page':
            self.passthrongh = True
            self.out = open(attrs.get('name')+'.html', 'w')
            self.out.write("<html><head>\n")
            self.out.write("<title>%s</title>\n" % attrs.get('title'))
            self.out.write('</head><body>\n')
        elif self.passthrongh:
            self.out.write("<"+name)
            for key, val in attrs.items():
                self.out.write(" %s='%s'" % (key, val))
            self.out.write('>')

    def endElement(self, name):
        if name == 'page':
            self.passthrongh = False
            self.out.write('\n</body></html>\n')
        elif self.passthrongh:
            self.out.write('</%s>' % name)

    def characters(self, chars):
        if self.passthrongh:
            self.out.write(chars)


parse('website.xml',PageMaker())