# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.parser.statements import block
from fcc.parser.base import split_statements
from fcc import ast


class FullCircleParser(object):
    def __init__(self, tokens=None):
        self.tokens = tokens

    def parse(self):
        self.root = ast.GlobalBlock(None)
        block(split_statements(self.tokens), self.root)
        return self.root
