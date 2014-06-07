# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.tokens.base import Token


class Constant(Token):
    """Represents a constant. The associated value may be inspected via the
    'value' attribute"""
    def __init__(self, value, line, column):
        self.value = value
        super(Constant, self).__init__(line, column)


class IntConstant(Constant):
    """Represents an integer constant"""
    def __repr__(self):
        return "%s(%d, %d, %d)" % (self.__class__.__name__, self.value,
                                   self.line, self.column)


class CharConstant(Constant):
    """Represents a character constant"""
    def __repr__(self):
        return "%s(%s, %d, %d)" % (self.__class__.__name__,
                                   self.value.encode("string-escape"),
                                   self.line, self.column)


class FloatConstant(Constant):
    """Represents a floating point constant"""
    def __repr__(self):
        return "%s(%s, %d, %d)" % (self.__class__.__name__, self.value,
                                   self.line, self.column)
