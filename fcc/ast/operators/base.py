# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.variables import VariableReference
from fcc.ast.base import Expression

# ---------
# operators
# ---------


class UnaryOperator(Expression):
    """An unary operator must have exactly one child, and that child must
    be an expression."""
    operand_type = Expression

    def validate(self):
        super(UnaryOperator, self).validate()

        assert len(self.children) == 1, "Parser error"
        assert isinstance(self.children[0], self.operand_type), \
            self.operand_type.name() + " expected"

    def generate(self, sp):
        osp = sp
        # first operand
        result, sp = self.children[0].generate(sp)
        assert sp - osp == self.operand_type.size, "Code generator error"

        # operator
        result.append(self.operation)
        return result, osp + self.size


class BinaryOperator(Expression):
    """A binary operator must have exactly two children, and those children
    must be expressions."""
    operand_type = Expression

    def validate(self):
        super(BinaryOperator, self).validate()

        assert len(self.children) == 2, "Parser error"
        for child in self.children:
            assert isinstance(child, self.operand_type), \
                self.operand_type.name() + " expected"
        self.first, self.second = self.children

    def generate(self, sp):
        osp = sp
        # first operand
        result, sp = self.first.generate(sp)
        assert sp - osp == self.operand_type.size, "Code generator error"

        # second operand
        code, sp = self.second.generate(sp)
        result.extend(code)
        assert sp - osp == 2 * self.operand_type.size, "Code generator error"

        # operator
        result.append(self.operation)
        return result, osp + self.size


class CommaOperator(BinaryOperator):
    """The comma operator evaluates both operands, but only keeps the
    right-most on the stack. Expressions don't have to be related to one
    another."""
    def generate(self, sp):
        osp = sp
        # evaluate and discard first operand
        result, sp = self.first.generate(sp)
        code, sp = self.first.release(sp)
        result.extend(code)
        assert sp == osp, "Code generator error"

        # second operand
        code, sp = self.second.generate(sp)
        result.extend(code)

        return result, sp


class AssignmentOperator(BinaryOperator):
    """An assignment operator is a binary operator where the first child is
    always a variable. The result of the expression is the new value of the
    variable."""
    def validate(self):
        super(AssignmentOperator, self).validate()

        assert isinstance(self.first, VariableReference), \
            "Variable expected"

    def generate(self, sp):
        osp = sp
        # evaluate expression
        result, sp = self.second.generate(sp)

        # pop data at variable address
        code, sp = self.pop(self.first.definition.addr(sp), sp)
        result.extend(code)

        # push data back onto the stack (it may very well be discarded on the
        # next instruction, but optimization is not the primary concern here)
        code, sp = self.push(self.first.definition.addr(sp), sp)
        result.extend(code)

        assert sp - osp == self.size, "Code generator error"
        return result, sp
