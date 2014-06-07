# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.expressions import (Expression, IntExpression, CharExpression,
                                 FloatExpression)
from fcc.ast.variables import (VariableDefinition, IntVariableDefinition,
                               CharVariableDefinition, FloatVariableDefinition)
from fcc.ast.base import Block, GlobalBlock, Statement

# ---------
# functions
# ---------


class FunctionDefinition(Block):
    """A function definition is a block that stores the function's name, type
    and argument list."""
    return_type = Expression

    def __init__(self, name, parent):
        assert isinstance(parent, GlobalBlock), \
            "Functions must be defined globally"

        super(FunctionDefinition, self).__init__(parent)

        self.name = name
        self.arguments = []
        self.return_address = IntVariableDefinition("__return_address__", self)
        self.children.pop()

        self.parent.add_symbol(name, self)

    def validate(self):
        super(FunctionDefinition, self).validate()

        # compute addresses
        sp = -self.return_address.expression_type.size
        self.return_address.sp = sp
        for arg in reversed(self.arguments):
            sp -= arg.expression_type.size
            arg.sp = sp

        if hasattr(self, "result"):
            sp -= self.return_type.size
            self.result.sp = sp

    def add_argument(self, name, expression_type):
        assert issubclass(expression_type, VariableDefinition)
        self.arguments.append(expression_type(name, self))
        self.children.pop()

    def assert_argument_list(self, arguments):
        for index, argument in enumerate(self.arguments):
            type_ = argument.expression_type
            assert isinstance(arguments[index], type_), \
                "Expected " + type_.name() + " for argument " + index

    @classmethod
    def name(self):
        return "void function"


class IntFunctionDefinition(FunctionDefinition):
    return_type = IntExpression

    def __init__(self, name, parent):
        super(IntFunctionDefinition, self).__init__(name, parent)

        self.result = IntVariableDefinition("__result__", self)
        self.children.pop()

    @classmethod
    def name(self):
        return "int function"


class CharFunctionDefinition(FunctionDefinition):
    return_type = CharExpression

    def __init__(self, name, parent):
        super(CharFunctionDefinition, self).__init__(name, parent)

        self.result = CharVariableDefinition("__result__", self)
        self.children.pop()

    @classmethod
    def name(self):
        return "char function"


class FloatFunctionDefinition(FunctionDefinition):
    return_type = FloatExpression

    def __init__(self, name, parent):
        super(FloatFunctionDefinition, self).__init__(name, parent)

        self.result = FloatVariableDefinition("__result__", self)
        self.children.pop()

    @classmethod
    def name(self):
        return "float function"


class FunctionCall(Statement):
    definition_type = FunctionDefinition

    def __init__(self, definition, parent):
        super(FunctionCall, self).__init__(parent)

        self.definition = definition

    def validate(self):
        super(FunctionCall, self).validate()

        self.definition.assert_argument_list(self.children)

    def generate(self, sp):
        osp = sp
        # allocate space for result if any
        result, sp = self.definition_type.return_type.alloc(sp)

        # push arguments
        for child in self.children:
            code, sp = child.generate(sp)
            result.extend(code)

        # determine total stack offset that needs to be cleaned up
        size = sp - osp - self.definition_type.return_type.size

        # use the procedure's definition as address placeholder before linking
        temp_addr = self.definition.name

        result.extend([
            ("loadi", 2),        # push 2
            ("puship", ),        # push ip
            ("addi", ),          # store ip + 2 as return address
            ("jmp", temp_addr),  # unconditional jump to function address
            ("release", size)    # rewind to initial stack size
        ])
        return result, osp + self.definition_type.return_type.size


class IntFunctionCall(FunctionCall, IntExpression):
    definition_type = IntFunctionDefinition


class CharFunctionCall(FunctionCall, CharExpression):
    definition_type = CharFunctionDefinition


class FloatFunctionCall(FunctionCall, FloatExpression):
    definition_type = FloatFunctionDefinition


class FunctionReturn(Statement):
    def __init__(self, parent):
        super(FunctionReturn, self).__init__(parent)

        parent = self.parent
        while parent is not None:
            if isinstance(parent, FunctionDefinition):
                self.definition = parent
                return
            parent = parent.parent
        assert False, "Return statements must be inside a function."

    def validate(self):
        super(FunctionReturn, self).validate()

        if self.definition.return_type is Expression:
            assert len(self.children) == 0, \
                "This function does not have a return value"
        else:
            assert len(self.children) == 1, "Expression expected"
            assert isinstance(self.children[0], self.definition.return_type), \
                self.definition.return_type.name() + " expected"

    def generate(self, sp):
        # determine result
        osp = sp
        result = []

        # pop result to its address if not void
        if hasattr(self.definition, "result"):
            code, sp = self.children[0].generate(sp)
            assert sp - osp == self.definition.return_type.size, \
                "Code generator error"
            result.extend(code)

            code, sp = self.definition.return_type.pop(
                self.definition.result.addr(sp), sp)
            assert sp == osp, "Code generation error"
            result.extend(code)

        # jump back to caller after clearing the stack
        code, sp = self.definition.finalize(osp)
        result.extend(code)
        result.append(("popip", ))
        return result, osp
