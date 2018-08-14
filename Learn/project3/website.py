# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-14 10:42:28
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-14 10:42:28
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os


class Dispatcher:
    def dispatch(self, prefix, name, attrs=None):
        manme = prefix+name.capitalize()
        dname = 'default'+prefix.capitalize()
        method = getattr(self, manme, None)
        if callable(method):
            args = []
        else:
            method = getattr(self, dname, None)
            args = name,
        if prefix == 'start':
            args += attrs,
        if callable(method):
            method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    def endElement(self, name):
        self.dispatch('end', name)


class WebsiteConstructor(Dispatcher, ContentHandler):
    passthrough = False

    def __init__(self, directory):
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        if not os.path.isdir(path):
            os.makedirs(path)

    def characters(self, chars):
        if self.passthrough:
            self.out.write(chars)

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<'+name)
            for key, val in attrs.items():
                self.out.write(" %s='%s'" % (key, val))
            self.out.write(">")

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write("</%s>" % name)

    def startDirectory(self, attrs):
        self.directory.append(attrs.get('name'))
        self.ensureDirectory()

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory+[attrs.get('name')+'.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs.get('title'))
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title):
        self.out.write('<html>\n<head>\n   <title>')
        self.out.write(title)
        self.out.write('</title>\n</head>\n    <body>\n')

    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')


parse('website.xml', WebsiteConstructor('public_html'))
