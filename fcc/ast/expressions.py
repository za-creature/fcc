# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.base import Expression

# -----------------
# typed expressions
# -----------------


class IntExpression(Expression):
    """An integer expression must push an int on the stack."""
    size = 4

    @classmethod
    def push(self, addr, sp):
        return [("pushi", addr)], sp + self.size

    @classmethod
    def pop(self, addr, sp):
        return [("popi", addr)], sp - self.size

    @classmethod
    def name(self):
        return "int expression"


class CharExpression(Expression):
    """A character expression must push a char on the stack."""
    size = 1

    @classmethod
    def push(self, addr, sp):
        return [("pushc", addr)], sp + self.size

    @classmethod
    def pop(self, addr, sp):
        return [("popc", addr)], sp - self.size

    @classmethod
    def name(self):
        return "char expression"


class FloatExpression(Expression):
    """A floating point expression must push a float on the stack."""
    size = 4

    @classmethod
    def push(self, addr, sp):
        return [("pushf", addr)], sp + self.size

    @classmethod
    def pop(self, addr, sp):
        return [("popf", addr)], sp - self.size

    @classmethod
    def name(self):
        return "float expression"

# --------------------
# constant expressions
# --------------------


class IntConstantExpression(IntExpression):
    def __init__(self, value, parent):
        assert isinstance(value, int), "Integer expected"
        self.value = value
        super(IntConstantExpression, self).__init__(parent)

    def generate(self, sp):
        return [("loadi", self.value)], sp + self.size


class CharConstantExpression(CharExpression):
    def __init__(self, value, parent):
        assert isinstance(value, str) and len(value) == 1, "Char expected"
        self.value = value
        super(CharConstantExpression, self).__init__(parent)

    def generate(self, sp):
        return [("loadc", self.value)], sp + self.size


class FloatConstantExpression(FloatExpression):
    def __init__(self, value, parent):
        assert isinstance(value, float), "Float expected"
        self.value = value
        super(FloatConstantExpression, self).__init__(parent)

    def generate(self, sp):
        return [("loadf", self.value)], sp + self.size
