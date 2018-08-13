# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-13 10:43:20
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-13 11:21:37


class Rule:
    """
    所有规则的基类
    """

    def action(self, block, handler):
        handler.start(self._type)
        handler.feed(block)
        handler.end(self._type)
        return True


class HeadingRule(Rule):
    """
    标题占一行，最多70个字符，并且不以冒号结尾
    """
    _type = 'heading'

    def condiciton(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(HeadingRule):
    """
    题目是文档的第一个大块，但前提是他是一个大标题
    """
    _type = 'title'
    first = True

    def condiciton(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condiciton(self, block)


class ListItemRule(Rule):
    """
    列表项是以连字符开始的段落。作为格式化的一部分,要移除连字符。
    """
    _type = 'listitem'

    def condiciton(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self._type)
        handler.feed(block[1:].strip())
        handler.end(self._type)
        return True


class ListRule(ListItemRule):
    """
    列表从不是列表项的块和随后的列表项之间。在最后一个连续列表项之后结束
    """
    _type = 'list'
    inside = False

    def condiciton(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and ListItemRule.condiciton(self, block):
            handler.start(self._type)
            self.inside = True
        elif self.inside and not ListItemRule.condiciton(self, block):
            handler.end(self._type)
            self.inside = False
        return False


class ParagrapheRule(Rule):
    """
    段落只是其他规则并没有覆盖到的块
    """
    _type = 'paragraph'

    def condiciton(self, block):
        return True
