# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.expressions import IntExpression, CharExpression, FloatExpression
from fcc.ast.base import Statement


# ----------
# statements
# ----------


class DiscardExpressionStatement(Statement):
    """A discard statement allows an expression to be evaluated just for its
    side effects (function calls). This is required because expressions always
    push something on the stack, and that stack must be cleaned up."""
    def validate(self):
        super(DiscardExpressionStatement, self).validate()

        assert len(self.children) == 1, "Parser error"
        self.expression = self.children[0]
        assert isinstance(self.expression, self.operand_type), \
            self.operand_type.name() + " expected"

    def generate(self, sp):
        osp = sp

        # evaluate expression
        result, sp = self.expression.generate(sp)
        assert sp - osp == self.operand_type.size, "Code generator error"

        # clear stack
        code, sp = self.operand_type.release(sp)
        result.extend(code)
        assert sp == osp, "Code generator error"

        return result, sp


class DiscardIntExpressionStatement(DiscardExpressionStatement):
    operand_type = IntExpression


class DiscardCharExpressionStatement(DiscardExpressionStatement):
    operand_type = CharExpression


class DiscardFloatExpressionStatement(DiscardExpressionStatement):
    operand_type = FloatExpression
