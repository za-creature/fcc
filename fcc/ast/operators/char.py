# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.operators.base import (UnaryOperator, BinaryOperator,
                                    AssignmentOperator)
from fcc.ast.expressions import CharExpression, IntExpression, FloatExpression

# -------------------
# character operators
# -------------------


class UnaryCharOperator(UnaryOperator):
    """An unary character operator must have exactly one child, and that
    child must be a character expression."""
    operand_type = CharExpression


class BinaryCharOperator(BinaryOperator):
    """A binary char operator must have exactly two children, and those
    children must be char expressions."""
    operand_type = CharExpression


class CharAssignment(AssignmentOperator, CharExpression):
    operand_type = CharExpression


class CharBacktick(UnaryCharOperator, CharExpression):
    operation = "printc",


# --------------------
# character arithmetic
# --------------------


class CharAddition(BinaryCharOperator, CharExpression):
    operation = "addc",


class CharSubstraction(BinaryCharOperator, CharExpression):
    operation = "subc",


class CharMultiplication(BinaryCharOperator, CharExpression):
    operation = "mulc",


class CharDivision(BinaryCharOperator, CharExpression):
    operation = "divc",


class CharModulus(BinaryCharOperator, CharExpression):
    operation = "modc",


class CharAdditiveNegation(UnaryCharOperator, CharExpression):
    operation = "negc",


# ----------------------------
# character bitwise operations
# ----------------------------


class CharBitwiseConjunction(BinaryCharOperator, CharExpression):
    operation = "bandc",


class CharBitwiseDisjunction(BinaryCharOperator, CharExpression):
    operation = "borc",


class CharExclusiveDisjunction(BinaryCharOperator, CharExpression):
    operation = "xorc",


class CharBitwiseNegation(UnaryCharOperator, CharExpression):
    operation = "bnotc",


class CharLeftShift(BinaryCharOperator, CharExpression):
    operation = "shli"


class CharRightShift(BinaryCharOperator, CharExpression):
    operation = "shri"


# ----------------------------
# character logical operations
# ----------------------------


class CharLogicalConjunction(BinaryCharOperator, CharExpression):
    operation = "landc",


class CharLogicalDisjunction(BinaryCharOperator, CharExpression):
    operation = "lorc",


class CharLogicalNegation(UnaryCharOperator, CharExpression):
    operation = "lnotc",


# ------------------------------
# character comparison operators
# ------------------------------


class CharEqualityComparison(BinaryCharOperator, CharExpression):
    operation = "eqc",


class CharInequalityComparison(BinaryCharOperator, CharExpression):
    operation = "neqc",


class CharGreaterThanComparison(BinaryCharOperator, CharExpression):
    operation = "gtc",


class CharGreaterThanOrEqualComparison(BinaryCharOperator, CharExpression):
    operation = "gtec",


class CharLessThanComparison(BinaryCharOperator, CharExpression):
    operation = "ltc",


class CharLessThanOrEqualComparison(BinaryCharOperator, CharExpression):
    operation = "ltec",


# ------------------------------
# character conversion operators
# ------------------------------


class CharToIntConversion(UnaryCharOperator, IntExpression):
    operation = "ctoi",


class CharToFloatConversion(UnaryCharOperator, FloatExpression):
    operation = "ctof",
