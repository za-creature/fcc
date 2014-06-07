# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.expressions import CharExpression
from fcc.ast.base import Statement


# ---------------
# loop statements
# ---------------


class WhileStatement(Statement):
    def validate(self):
        super(WhileStatement, self).validate()

        assert len(self.children) == 2, "Parser error"
        assert isinstance(self.children[0], CharExpression), \
            "char expression expected"
        assert isinstance(self.children[1], Statement), \
            "Statement expected"

    def generate(self, sp):
        osp = sp
        # evaluate condition
        result, sp = self.children[0].generate(sp)
        assert sp - osp == CharExpression.size, "Code generator error"

        # generate the 'repeated' block
        loop, sp = self.children[1].generate(osp)
        assert sp == osp, "Code generator error"
        # add an unconditional jump to re-evaluate the condition after the
        # block is executed
        loop.append(("jmpr", -len(loop) - len(result) - 2))

        # add a conditional jump after the expression is evaluated to test
        # whether the loop should be broken or not
        result.append(("jmp0r", len(loop)))
        result.extend(loop)

        return result, osp
