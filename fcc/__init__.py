# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.lexer import FullCircleLexer
from fcc.parser import FullCircleParser
from fcc.vm import FullCircleVirtualMachine


def lex(data):
    return FullCircleLexer(data).lex()


def parse(tokens):
    return FullCircleParser(tokens).parse()


def compile(root):
    root.validate()
    return root.generate(0)[0]


def run(bytecode, stack=65536):
    FullCircleVirtualMachine(bytecode).run(stack)


__all__ = ["FullCircleLexer", "FullCircleParser", "FullCircleVirtualMachine",
           "lex", "parse", "compile", "run"]
