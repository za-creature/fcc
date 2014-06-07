# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

# ------------
# base classes
# ------------


class Statement(object):
    """A statement is the smallest standalone element. A statement may contain
    0 or more sub statements that must be executed in order."""
    def __init__(self, parent):
        self.parent = parent
        self.children = []

        if parent:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def replace_child(self, old, new, move_children=True):
        self.children[self.children.index(old)] = new

        old.parent = None
        new.parent = self

        if move_children:
            for child in old.children:
                new.add_child(child)

    def validate(self):
        for child in self.children:
            assert isinstance(child, Statement), "Statement expected"
            child.validate()

    def generate(self, sp):
        """Returns a virtual machine code fragment that will execute this
        statement. 'sp' is the stack pointer on block entry."""
        return [("nop", )], sp

    def __repr__(self):
        if self.children:
            return "%s: %s" % (self.__class__.__name__, self.children)
        return self.__class__.__name__


class Expression(Statement):
    """An expression must push something on the stack."""
    size = 0

    @classmethod
    def push(self, addr, sp):
        return [("nop",)], sp

    @classmethod
    def pop(self, addr, sp):
        return [("nop",)], sp

    @classmethod
    def alloc(self, sp):
        return [("alloc", self.size)], sp + self.size

    @classmethod
    def release(self, sp):
        if self.size:
            return [("release", self.size)], sp - self.size
        return [], sp

    @classmethod
    def name(self):
        return "void* expression"


class Block(Statement):
    """A block is a statement that may contain other statements (including
    other blocks). Any variables declared inside a block may only be accessed
    from within itself."""
    def __init__(self, parent):
        self.symbols = {}
        super(Block, self).__init__(parent)

    def add_symbol(self, name, definition):
        assert name not in self.symbols, "Duplicate identifier"
        self.symbols[name] = definition

    def validate(self):
        super(Block, self).validate()

        for child in self.children:
            assert not isinstance(child, Expression), "Statement expected"

    def generate(self, sp):
        result = []
        self.sp = sp

        # execute all child statements
        for child in self.children:
            code, sp = child.generate(sp)
            result.extend(code)

        # clear stack
        code, sp = self.finalize(sp)
        result.extend(code)

        return result, self.sp

    def finalize(self, sp):
        """Called to revert stack position to the initial value upon entering
        the block. Must be called after `generate` and with the current stack
        pointer."""
        if sp != self.sp:
            return [("release", sp - self.sp)], self.sp
        return [], sp


class GlobalBlock(Block):
    """The global block stores all procedures, functions and global variables.
    It must always be the root of the parse tree."""
    def __init__(self, parent):
        super(GlobalBlock, self).__init__(parent)

    def validate(self):
        super(GlobalBlock, self).validate()
        assert self.parent is None, "Parser error"

        from fcc.ast.variables import VariableDefinition
        from fcc.ast.functions import FunctionDefinition
        self.func_type = FunctionDefinition

        assert "main" in self.symbols, "No 'main' function defined"
        assert isinstance(self.symbols["main"], FunctionDefinition), \
            "Global 'main' symbol must be a function"

        for child in self.children:
            assert isinstance(child, (VariableDefinition,
                                      FunctionDefinition)), \
                "Statements not allowed in global scope"

    def generate(self, sp):
        result = []
        self.sp = sp

        for child in self.children:
            # build child code
            code, sp = child.generate(sp)

            if isinstance(child, self.func_type):
                # do not explicitly execute functions except 'main'
                if child.name == "main":
                    result.append(("loadi", "__exit__"))
                else:
                    result.append(("jmpr", len(code)))

                # store function address and add bytecode
                self.symbols[child.name] = len(result)

            # append child code
            result.extend(code)

        # 'main' will end up here, so pop the ip
        result.append(("release", 4))
        self.symbols["__exit__"] = len(result) - 1

        # clear stack
        code, sp = self.finalize(sp)
        result.extend(code)

        # solve dangling references
        for index, operation in enumerate(result):
            if operation[0] in ("loadi", "jmp", "jmp0", "jmp1") and \
                    isinstance(operation[1], (str, unicode)):
                try:
                    result[index] = (operation[0], self.symbols[operation[1]])
                except KeyError:
                    assert False, "Undefined reference '%s'" % operation[1]

        return result, self.sp
