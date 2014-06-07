# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.parser.expressions import expression, promote
from fcc.parser.base import split, var_type, func_type, ParserError
from fcc import tokens
from fcc import ast


def function(header, body, parent):
    if not isinstance(parent, ast.GlobalBlock):
        raise ParserError("Functions must be defined globally")

    constructor = func_type(header[0])

    if not isinstance(header[-1], tokens.CloseParanthesisOperator):
        raise ParserError(header[-1], ") expected")

    function = constructor(header[1].name, parent)

    # add arguments if any
    for spec in split(header[3:-1], tokens.CommaOperator):
        if len(spec) != 2:
            raise ParserError(spec[0], "Invalid syntax")
        if not isinstance(spec[1], tokens.Identifier):
            raise ParserError(spec[1], "Identifier expected")
        function.add_argument(spec[1].name, var_type(spec[0]))

    if header[1].name == "main":
        if not isinstance(header[0], tokens.VoidKeyword):
            raise ParserError(header[0], "'main' function must be void")
        if function.arguments:
            raise ParserError(header[3], "'main' function may not have"
                                         "arguments")

    block(body, function)


def variable(statement, parent):
    constructor = var_type(statement[0])

    # split the statement at comma boundary
    for spec in split(statement[1:], tokens.CommaOperator):
        if not spec or not isinstance(spec[0], tokens.Identifier):
            raise ParserError(spec[0], "Identifier expected")

        # assume variable is uninitialized by default
        variable = constructor(spec[0].name, parent)

        if len(spec) > 1:
            # variable contains initialization code
            if not isinstance(spec[1], tokens.AssignmentOperator):
                raise ParserError(spec[1], "= or , expected")
            if len(spec) < 2:
                raise ParserError(spec[2], "Expression expected")

            expression(spec[2:], variable)


def _return(fragment, parent):
    node = ast.FunctionReturn(parent)
    if fragment:
        expression(fragment, node)


def block(fragment, parent):
    skip = 0
    for index, statement in enumerate(fragment):
        if not statement:
            continue  # skip empty statements

        if skip:
            skip -= 1
            continue  # skip already processed statements

        if isinstance(statement[0], (tokens.IntKeyword,
                                     tokens.CharKeyword,
                                     tokens.FloatKeyword,
                                     tokens.VoidKeyword)):
            # declaration
            if len(statement) < 2:
                raise ParserError(statement[0], "Identifier expected")
            if not isinstance(statement[1], tokens.Identifier):
                raise ParserError(statement[1], "Identifier expected")

            if \
                    len(statement) > 2 and \
                    isinstance(statement[2], tokens.OpenParanthesisOperator):
                try:
                    if not isinstance(fragment[index+1][0], list):
                        raise ParserError(fragment[index+1], "Block expected")
                except IndexError:
                    raise ParserError(fragment[-1], "Unexpected end of file")

                function(statement, fragment[index+1], parent)
                skip = 1
            else:
                variable(statement, parent)
        elif isinstance(statement[0], tokens.IfKeyword):
            # conditional statement
            result = ast.IfStatement(parent)
            expression(statement[1:], result)

            # get condition statement
            try:
                child = ast.Block(result)
                if fragment[index+1] and \
                        isinstance(fragment[index+1][0], list):
                    block(fragment[index+1], child)
                else:
                    block([fragment[index+1]], child)
                skip = 1
            except IndexError:
                raise ParserError(fragment[-1], "Statement expected")

            # check for non-trivial else keyword
            if index + 2 < len(fragment) and fragment[index+2] and \
                    isinstance(fragment[index+2][0], tokens.ElseKeyword):
                try:
                    if fragment[index+3]:
                        child = ast.Block(result)
                        if isinstance(fragment[index+3][0], list):
                            block(fragment[index+3], child)
                        else:
                            block([fragment[index+3]], child)
                    skip = 3
                except IndexError:
                    raise ParserError(fragment[-1], "Statement expected")
        elif isinstance(statement[0], tokens.ReturnKeyword):
            _return(statement[1:], parent)
        elif isinstance(statement[0], tokens.ForKeyword):
            # for loops are automatically converted into while loops
            try:
                init, cond, step = split(statement[2:-1],
                                         tokens.SemicolonToken)
            except ValueError:
                raise ParserError(fragment[-1], "Invalid syntax")

            result = ast.Block(parent)
            block([init], result)

            loop = ast.WhileStatement(result)
            expression(cond, loop)
            inner = ast.Block(loop)

            try:
                if fragment[index+1] and \
                        isinstance(fragment[index+1][0], list):
                    block(fragment[index+1], inner)
                else:
                    block([fragment[index+1]], inner)
                skip = 1
            except IndexError:
                raise ParserError(fragment[-1], "Statement expected")

            block([step], inner)
        elif isinstance(statement[0], tokens.WhileKeyword):
            # while loops are implemented directly via the while statement
            result = ast.WhileStatement(parent)
            expression(statement[1:], result)
            # get loop statement
            try:
                child = ast.Block(result)
                if fragment[index+1] and \
                        isinstance(fragment[index+1][0], list):
                    block(fragment[index+1], child)
                else:
                    block([fragment[index+1]], child)
                skip = 1
            except IndexError:
                raise ParserError(fragment[-1], "Statement expected")
        elif isinstance(statement[0], list):
            # unbound sub-block
            child = ast.Block(parent)
            block(statement, child)
        else:
            # anything else must be an expression; convert to discard statement
            temp = ast.UnaryOperator(parent)
            expression(statement, temp)

            promote(temp, (ast.DiscardCharExpressionStatement,
                           ast.DiscardIntExpressionStatement,
                           ast.DiscardFloatExpressionStatement))
