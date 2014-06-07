# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.expressions import (Expression, IntExpression, CharExpression,
                                 FloatExpression)
from fcc.ast.base import Statement, Block, GlobalBlock

# ---------
# variables
# ---------


class VariableDefinition(Statement):
    """A variable definition must reserve stack space for one variable, and
    must remember its stack offset in the current block. In addition to that,
    it stores the variable's name. A variable definition may optionally have a
    default value that can be an expression. Otherwise, the default value is
    not guaranteed (in practice, global variables are always 0 filled)."""
    def __init__(self, name, parent):
        self.name = name
        assert isinstance(parent, Block), \
            "Variables must be defined inside a block"
        parent.add_symbol(name, self)
        super(VariableDefinition, self).__init__(parent)

    def validate(self):
        super(VariableDefinition, self).validate()

        assert len(self.children) < 2, "Invalid syntax"
        if len(self.children):
            assert isinstance(self.children[0], self.expression_type), \
                self.expression_type.name() + " expected"

    def generate(self, sp):
        self.sp = sp
        if len(self.children):
            # variable has a default value
            return self.children[0].generate(sp)
        else:
            # variable is uninitialized
            return self.expression_type.alloc(sp)

    def addr(self, sp):
        if isinstance(self.parent, GlobalBlock):
            # global variable
            return self.sp
        else:
            # local variable; return stack offset
            return self.sp - sp


class IntVariableDefinition(VariableDefinition):
    expression_type = IntExpression


class CharVariableDefinition(VariableDefinition):
    expression_type = CharExpression


class FloatVariableDefinition(VariableDefinition):
    expression_type = FloatExpression


class VariableReference(Expression):
    """A variable reference simply points to a variable definition. It may be
    used as an expression, or as the target of an assign statement."""
    def __init__(self, definition, parent):
        self.definition = definition
        super(VariableReference, self).__init__(parent)

    def validate(self):
        super(VariableReference, self).validate()

        assert len(self.children) == 0, "Parser error"
        assert isinstance(self.definition, self.definition_type), \
            self.definition_type.expression_type.name() + " expected"

    def generate(self, sp):
        type_ = self.definition_type.expression_type
        return type_.push(self.definition.addr(sp), sp)


class IntVariableReference(VariableReference, IntExpression):
    definition_type = IntVariableDefinition


class CharVariableReference(VariableReference, CharExpression):
    definition_type = CharVariableDefinition


class FloatVariableReference(VariableReference, FloatExpression):
    definition_type = FloatVariableDefinition
