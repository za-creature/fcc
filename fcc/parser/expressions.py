# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.parser.base import startswith, ParserError
from fcc import tokens
from fcc import ast

from operator import lt, le
from sys import maxint


def promote(operator, promotions):
    for promotion in promotions:
        if isinstance(operator.children[0], promotion.operand_type):
            return operator.parent.replace_child(operator, promotion(None))
    raise ParserError(None, "Unable to promote operator " + operator)


def function(fragment, parent):
    # get function reference
    p = parent
    while p is not None:
        if isinstance(p, ast.GlobalBlock) and fragment[0].name in p.symbols:
            function = p.symbols[fragment[0].name]
            if not isinstance(function, ast.FunctionDefinition):
                raise ParserError(fragment[0], "Function expected")
            break
        p = p.parent
    else:
        raise ParserError(fragment[0],
                          "Undefined identifier '" + fragment[0].name + "'")

    for name in ("IntFunction", "FloatFunction", "CharFunction", "Function"):
        if isinstance(function, getattr(ast, name + "Definition")):
            result = getattr(ast, name + "Call")(function, parent)
            break
    else:
        raise ParserError(fragment[0], "Unknown function type")

    # add arguments
    spec = []
    depth = 0
    for token in fragment[2:-1]:
        if depth:
            spec.append(token)
            if isinstance(token, (tokens.FunctionApplicationOperator,
                                  tokens.OpenParanthesisOperator)):
                depth += 1
            elif isinstance(token, tokens.CloseParanthesisOperator):
                depth -= 1
        else:
            if isinstance(token, (tokens.FunctionApplicationOperator,
                                  tokens.OpenParanthesisOperator)):
                depth += 1

            if isinstance(token, tokens.CommaOperator):
                expression(spec, result)
                spec = []
            else:
                spec.append(token)
    if spec:
        expression(spec, result)


def assignment(fragment, offset, parent):
    # check lvalue of an assignment is a variable
    if not isinstance(fragment[offset-1], tokens.Identifier):
        raise ParserError(fragment[offset-1], "Variable expected")

    temp = ast.BinaryOperator(parent)

    variable(fragment[offset-1:offset], temp)

    for operator in ["Addition", "Substraction", "Multiplication", "Division",
                     "Modulus", "BitwiseConjunction", "BitwiseDisjunction",
                     "ExclusiveDisjunction", "LeftShift", "RightShift"]:
        # compound assignment operator; replace with basic operator
        if isinstance(fragment[offset],
                      getattr(tokens, operator + "AssignmentOperator")):
            fragment[offset] = getattr(tokens, operator + "Operator")(
                fragment[offset].line,
                fragment[offset].column)
            binary(fragment[offset-1:], offset, temp)
            break
    else:
        # simple assignment operator
        expression(fragment[offset+1:], temp)

    return promote(temp, (ast.CharAssignment,
                          ast.IntAssignment,
                          ast.FloatAssignment))


def binary(fragment, offset, parent):
    temp = ast.BinaryOperator(parent)
    expression(fragment[:offset], temp)
    expression(fragment[offset+1:], temp)

    for operator, promotions in [
        (tokens.AdditionOperator, (ast.CharAddition,
                                   ast.IntAddition,
                                   ast.FloatAddition)),
        (tokens.SubstractionOperator, (ast.CharSubstraction,
                                       ast.IntSubstraction,
                                       ast.FloatSubstraction)),
        (tokens.MultiplicationOperator, (ast.CharMultiplication,
                                         ast.IntMultiplication,
                                         ast.FloatMultiplication)),
        (tokens.DivisionOperator, (ast.CharDivision,
                                   ast.IntDivision,
                                   ast.FloatDivision)),
        (tokens.ModulusOperator, (ast.CharModulus,
                                  ast.IntModulus)),
        (tokens.BitwiseConjunctionOperator, (ast.CharBitwiseConjunction,
                                             ast.IntBitwiseConjunction)),
        (tokens.BitwiseDisjunctionOperator, (ast.CharBitwiseDisjunction,
                                             ast.IntBitwiseDisjunction)),
        (tokens.ExclusiveDisjunctionOperator, (ast.CharExclusiveDisjunction,
                                               ast.IntExclusiveDisjunction)),
        (tokens.LeftShiftOperator, (ast.CharLeftShift,
                                    ast.IntLeftShift)),
        (tokens.RightShiftOperator, (ast.CharRightShift,
                                     ast.IntRightShift)),
        (tokens.EqualityOperator, (ast.CharEqualityComparison,
                                   ast.IntEqualityComparison,
                                   ast.FloatEqualityComparison)),
        (tokens.InequalityOperator, (ast.CharInequalityComparison,
                                     ast.IntInequalityComparison,
                                     ast.FloatInequalityComparison)),
        (tokens.GreaterThanOperator, (ast.CharGreaterThanComparison,
                                      ast.IntGreaterThanComparison,
                                      ast.FloatGreaterThanComparison)),
        (tokens.GreaterThanOrEqualOperator, (
            ast.CharGreaterThanOrEqualComparison,
            ast.IntGreaterThanOrEqualComparison,
            ast.FloatGreaterThanOrEqualComparison)),
        (tokens.LessThanOperator, (ast.CharLessThanComparison,
                                   ast.IntLessThanComparison,
                                   ast.FloatLessThanComparison)),
        (tokens.LessThanOrEqualOperator, (ast.CharLessThanOrEqualComparison,
                                          ast.IntLessThanOrEqualComparison,
                                          ast.FloatLessThanOrEqualComparison)),
        (tokens.LogicalConjunctionOperator, (ast.CharLogicalConjunction,
                                             ast.IntLogicalConjunction,
                                             ast.FloatLogicalConjunction)),
        (tokens.LogicalDisjunctionOperator, (ast.CharLogicalDisjunction,
                                             ast.IntLogicalDisjunction,
                                             ast.FloatLogicalDisjunction))
    ]:
        if isinstance(fragment[offset], operator):
            return promote(temp, promotions)
    raise ParserError(fragment[offset],
                      "Illegal arguments to " + str(fragment[offset]))


def unary(fragment, offset, parent):
    temp = ast.UnaryOperator(parent)

    if isinstance(fragment[offset], tokens.IncrementOperator):
        if offset > 0 and (fragment[offset-1], tokens.Identifier):
            # var++
            variable(fragment[offset-1:offset], temp)
            return promote(temp, (ast.CharSuffixIncrement,
                                  ast.IntSuffixIncrement,
                                  ast.FloatSuffixIncrement))
        elif offset < len(fragment) and isinstance(fragment[offset+1],
                                                   tokens.Identifier):
            # ++var
            variable(fragment[offset+1:offset+2], temp)
            return promote(temp, (ast.CharPrefixIncrement,
                                  ast.IntPrefixIncrement,
                                  ast.FloatPrefixIncrement))
        else:
            raise SyntaxError(fragment[offset], "Variable expected")
    elif isinstance(fragment[offset], tokens.FullCircleBacktickOperator):
        # `expr
        expression(fragment[offset+1:], temp)
        return promote(temp, (ast.CharBacktick,
                              ast.IntBacktick,
                              ast.FloatBacktick))
    elif isinstance(fragment[offset], tokens.BitwiseNegationOperator):
        # ~expr
        expression(fragment[offset+1:], temp)
        return promote(temp, (ast.CharBitwiseNegation,
                              ast.IntBitwiseNegation))
    elif isinstance(fragment[offset], tokens.LogicalNegationOperator):
        # !expr
        expression(fragment[offset+1:], temp)
        return promote(temp, (ast.CharLogicalNegation,
                              ast.IntLogicalNegation,
                              ast.FloatLogicalNegation))
    else:
        raise ParserError(fragment[offset], "Unknown operator")


def _operator(fragment, offset, parent):
    if isinstance(fragment[offset], tokens.FunctionApplicationOperator):
        if not isinstance(fragment[offset-1], tokens.Identifier):
            raise ParserError("Identifier expected")
        # find out where the function ends
        depth = 0
        for end, token in fragment[offset:]:
            if isinstance(token, (tokens.FunctionApplicationOperator,
                                  tokens.OpenParanthesisOperator)):
                depth += 1
            elif isinstance(token, tokens.CloseParanthesisOperator):
                depth -= 1
                if depth == 0:
                    break
        else:
            raise ParserError(token, ") expected")

    if isinstance(fragment[offset], tokens.BinaryOperator):
        # split into two subexpressions at offset
        if offset == 0:
            raise ParserError(fragment[offset], "No left value for binary "
                                                "operator")

        if isinstance(fragment[offset], tokens.AssignmentOperator):
            assignment(fragment, offset, parent)
        else:
            binary(fragment, offset, parent)
    elif isinstance(fragment[offset], tokens.UnaryOperator):
        unary(fragment, offset, parent)
    else:
        raise ParserError(fragment[offset], "Operator expected")


def variable(fragment, parent):
    # get variable reference from parent scope
    p = parent
    while p is not None:
        if isinstance(p, ast.Block) and fragment[0].name in p.symbols:
            variable = p.symbols[fragment[0].name]
            if not isinstance(variable, ast.VariableDefinition):
                raise ParserError(fragment[0], "Variable expected")
            break
        p = p.parent
    else:
        raise ParserError(fragment[0],
                          "Undefined identifier '" + fragment[0].name + "'")

    # convert variable name into a reference to it's definition
    if isinstance(variable, ast.IntVariableDefinition):
        return ast.IntVariableReference(variable, parent)
    elif isinstance(variable, ast.CharVariableDefinition):
        return ast.CharVariableReference(variable, parent)
    elif isinstance(variable, ast.FloatVariableDefinition):
        return ast.FloatVariableReference(variable, parent)


def constant(fragment, parent):
    if isinstance(fragment[0], tokens.IntConstant):
        return ast.IntConstantExpression(fragment[0].value, parent)
    elif isinstance(fragment[0], tokens.CharConstant):
        return ast.CharConstantExpression(fragment[0].value, parent)
    elif isinstance(fragment[0], tokens.FloatConstant):
        return ast.FloatConstantExpression(fragment[0].value, parent)
    raise ParserError(fragment[0], "Unsupported constant type")


def expression(fragment, parent):
    min = maxint
    min_id = -1
    offset = 0

    prev = None

    for index, token in enumerate(fragment):
        # get the operator with the lowest precedence
        if isinstance(token, tokens.Operator):
            if isinstance(token, (tokens.FunctionApplicationOperator)):
                offset += 1
            if isinstance(token, (tokens.OpenParanthesisOperator)):
                offset += 1
                if isinstance(prev, tokens.Identifier):
                    fragment[index] = tokens.FunctionApplicationOperator(
                        token.line, token.column)
                    token = fragment[index]
                else:
                    prev = token
                    continue
            elif isinstance(token, (tokens.CloseParanthesisOperator)):
                if offset <= 0:
                    raise ParserError(token, "Unexpected )")
                offset -= 1
                prev = token
                continue

            for precedence, (operator, comparator) in enumerate([
                (tokens.CommaOperator, le),
                (tokens.FullCircleBacktickOperator, lt),
                # assignment
                (tokens.AssignmentOperator, lt),
                # bitwise and logic
                (tokens.LogicalDisjunctionOperator, le),
                (tokens.LogicalConjunctionOperator, le),
                (tokens.BitwiseDisjunctionOperator, le),
                (tokens.ExclusiveDisjunctionOperator, le),
                (tokens.BitwiseConjunctionOperator, le),
                ((tokens.EqualityOperator,
                  tokens.InequalityOperator), le),
                # comparison
                ((tokens.GreaterThanOperator,
                  tokens.GreaterThanOrEqualOperator,
                  tokens.LessThanOperator,
                  tokens.LessThanOrEqualOperator), le),
                # math
                ((tokens.LeftShiftOperator,
                  tokens.RightShiftOperator), le),
                ((tokens.AdditionOperator,
                  tokens.SubstractionOperator), le),
                ((tokens.MultiplicationOperator,
                  tokens.DivisionOperator,
                  tokens.ModulusOperator), le),
                # unary operators
                (tokens.UnaryOperator, lt),
                (tokens.FunctionApplicationOperator, le)
            ]):
                if isinstance(token, operator):
                    precedence += 1000 * offset
                    if comparator(precedence, min):
                        min = precedence
                        min_id = index
                    break
            else:
                raise ParserError(token,
                                  "Illegal / unsupported token: " + str(token))
        prev = token

    if offset > 0:
        raise ParserError(fragment[-1], ") expected")
    if min_id == -1:
        # no operators found; expression must be either an identifier, a
        # constant, or a call to a function without arguments

        if len(fragment) == 1:
            # constant or variable
            if isinstance(fragment[0], tokens.Identifier):
                return variable(fragment, parent)
            elif isinstance(fragment[0], tokens.Constant):
                return constant(fragment, parent)
            else:
                raise ParserError(fragment[0],
                                  "Identifier or constant expected")
        elif len(fragment) == 3:
            if startswith(fragment, (tokens.Identifier,
                                     tokens.OpenParanthesisOperator,
                                     tokens.CloseParanthesisOperator)):
                # argument-less function call
                return function(fragment, parent)
            elif isinstance(fragment[0], tokens.OpenParanthesisOperator) and \
                    isinstance(fragment[-1], tokens.CloseParanthesisOperator):
                # constant or variable wrapped in paranthesis
                return expression(fragment[1:-1], parent)
            else:
                raise ParserError(fragment[0], "Invalid syntax")
        else:
            raise ParserError(fragment[0], "Operator expected")
    elif min < 1000:
        # if the lowest precedence operator is less than 1000, split the
        # expression into two subexpressions at said operator
        return _operator(fragment, min_id, parent)
    else:
        if startswith(fragment, (tokens.Identifier,
                                 tokens.FunctionApplicationOperator)):
            # the fragment is a function call
            return function(fragment, parent)
        elif isinstance(fragment[0], tokens.OpenParanthesisOperator) and \
                isinstance(fragment[-1], tokens.CloseParanthesisOperator):
            # the fragment is wrapped in paranthesis
            return expression(fragment[1:-1], parent)
        else:
            raise ParserError(fragment[0], "Invalid syntax")
