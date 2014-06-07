# coding=utf-8
from __future__ import absolute_import, unicode_literals, division


class Token(object):
    """The base class for every token"""
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __repr__(self):
        return "%s(%d, %d)" % (self.__class__.__name__, self.line, self.column)


class Identifier(Token):
    def __init__(self, name, line, column):
        self.name = name
        super(Identifier, self).__init__(line, column)

    def __repr__(self):
        return "%s(%s, %d, %d)" % (self.__class__.__name__, self.name,
                                   self.line, self.column)


class BlockStartToken(Token):
    """Represents the '{' start of a block"""


class BlockEndToken(Token):
    """Represents the '}' end of a block"""


class SemicolonToken(Token):
    """Represents the ';' semicolon token"""
