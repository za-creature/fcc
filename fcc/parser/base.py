# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc import tokens
from fcc import ast


class ParserError(Exception):
    pass


def split(tokens, separator):
    result = []
    chunk = []
    for token in tokens:
        if isinstance(token, separator):
            result.append(chunk)
            chunk = []
        else:
            chunk.append(token)
    # add last chunk
    if chunk:
        result.append(chunk)
    return result


def split_statements(fragment):
    """Splits the lexer output into statements. Statements are separated by
    ;, { or by }. { marks the start of a block, which is a statement by itself.
    """

    stack = [[]]
    depth = -1
    statement = []
    for index, token in enumerate(fragment):
        def semicolon_expected():
            if statement:
                raise ParserError(fragment[index-1], "Expected ; before " +
                                                     str(token))

        if depth != -1:
            # in a if / for / while construct
            statement.append(token)
            if isinstance(token, tokens.OpenParanthesisOperator):
                depth += 1
            elif isinstance(token, tokens.CloseParanthesisOperator):
                depth -= 1
                if not depth:
                    # end of construct
                    stack[-1].append(statement)
                    statement = []
                    depth = -1
        else:
            if isinstance(token, tokens.SemicolonToken):
                # end of statement; add it to the deep-most lbock
                stack[-1].append(statement)
                statement = []
            elif isinstance(token, tokens.BlockStartToken):
                if startswith(statement, [(tokens.IntKeyword,
                                           tokens.CharKeyword,
                                           tokens.FloatKeyword,
                                           tokens.VoidKeyword),
                                          tokens.Identifier,
                                          tokens.OpenParanthesisOperator]):
                    # previous token was a function definition
                    stack[-1].append(statement)
                    statement = []
                else:
                    semicolon_expected()
                # create a new block on the stack
                stack.append([])
            elif isinstance(token, tokens.BlockEndToken):
                semicolon_expected()
                # pop the deep-most block and append it to its parent
                try:
                    child = stack.pop()
                    stack[-1].append(child)
                except IndexError:
                    raise ParserError(token, "Unexpected }")
            elif isinstance(token, (tokens.IfKeyword,
                                    tokens.ForKeyword,
                                    tokens.WhileKeyword)):
                semicolon_expected()
                # enter if / for / while construct
                try:
                    if not isinstance(fragment[index+1],
                                      tokens.OpenParanthesisOperator):
                        raise ParserError(fragment[index+1], "( expected")
                except IndexError:
                    raise ParserError(fragment[-1], "Unexpected end of file")

                statement.append(token)
                depth = 0
            elif isinstance(token, (tokens.DoKeyword,
                                    tokens.ElseKeyword)):
                semicolon_expected()
                # do and else are single-keyword tokens
                stack[-1].append([token])
            else:
                # standard token
                statement.append(token)

    if len(stack) != 1 or depth != -1:
        raise ParserError(fragment[-1], "Unexpected end of file")

    return stack[0]


def startswith(tokens, pattern):
    if len(tokens) < len(pattern):
        return False

    for index, token_class in enumerate(pattern):
        if not isinstance(tokens[index], token_class):
            return False
    return True


def var_type(token):
    for cls, result in [(tokens.IntKeyword, ast.IntVariableDefinition),
                        (tokens.FloatKeyword, ast.FloatVariableDefinition),
                        (tokens.CharKeyword, ast.CharVariableDefinition)]:
        if isinstance(token, cls):
            return result
    raise ParserError(token, "Invalid variable type")


def func_type(token):
    for cls, result in [(tokens.IntKeyword, ast.IntFunctionDefinition),
                        (tokens.CharKeyword, ast.CharFunctionDefinition),
                        (tokens.FloatKeyword, ast.FloatFunctionDefinition),
                        (tokens.VoidKeyword, ast.FunctionDefinition)]:
        if isinstance(token, cls):
            return result
    raise ParserError(token, "Invalid function return type")
