# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.expressions import CharExpression
from fcc.ast.base import Statement

# ----------------------
# conditional statements
# ----------------------


class IfStatement(Statement):
    def validate(self):
        super(IfStatement, self).validate()

        assert len(self.children) < 4, "Parser error"
        assert isinstance(self.children[0], CharExpression), \
            "char expression expected"
        assert isinstance(self.children[1], Statement), \
            "Statement expected"
        if len(self.children) == 3:
            assert isinstance(self.children[2], Statement), \
                "Statement expected"

    def generate(self, sp):
        osp = sp
        # evaluate condition
        result, sp = self.children[0].generate(sp)
        assert sp - osp == CharExpression.size, "Code generator error"

        # generate the 'then' block
        then, sp = self.children[1].generate(osp)
        assert sp == osp, "Code generator error"

        # generate the 'else' block if any
        if len(self.children) == 3:
            _else, sp = self.children[2].generate(osp)
            assert sp == osp, "Code generator error"

            # make sure that the 'then' branch skips the 'else' branch after it
            # is executed
            then.append(("jmpr", len(_else)))

        # add the conditional jump; if the condition is false, jump to the end
        # of the 'then' branch (which will be either the start of the 'else'
        # branch, or the following statement)
        result.append(("jmp0r", len(then)))
        result.extend(then)
        if len(self.children) == 3:
            result.extend(_else)

        return result, osp
