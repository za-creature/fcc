# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.operators.base import (UnaryOperator, BinaryOperator,
                                    AssignmentOperator)
from fcc.ast.expressions import CharExpression, IntExpression, FloatExpression

# -----------------
# integer operators
# -----------------


class UnaryIntOperator(UnaryOperator):
    """A binary int operator must have exactly one child, and that child
    must be a int expression."""
    operand_type = IntExpression


class BinaryIntOperator(BinaryOperator):
    """A binary int operator must have exactly two children, and those children
    must be int expressions."""
    operand_type = IntExpression


class IntAssignment(AssignmentOperator, IntExpression):
    operand_type = IntExpression


class IntBacktick(UnaryIntOperator, IntExpression):
    operation = "printi",


# ------------------
# integer arithmetic
# ------------------


class IntAddition(BinaryIntOperator, IntExpression):
    operation = "addi",


class IntSubstraction(BinaryIntOperator, IntExpression):
    operation = "subi",


class IntMultiplication(BinaryIntOperator, IntExpression):
    operation = "muli",


class IntDivision(BinaryIntOperator, IntExpression):
    operation = "divi",


class IntModulus(BinaryIntOperator, IntExpression):
    operation = "modi",


class IntAdditiveNegation(UnaryIntOperator, IntExpression):
    operation = "negi",


# --------------------------
# integer bitwise operations
# --------------------------


class IntBitwiseConjunction(BinaryIntOperator, IntExpression):
    operation = "bandi",


class IntBitwiseDisjunction(BinaryIntOperator, IntExpression):
    operation = "bori",


class IntExclusiveDisjunction(BinaryIntOperator, IntExpression):
    operation = "xori",


class IntBitwiseNegation(UnaryIntOperator, IntExpression):
    operation = "bnoti",


class IntLeftShift(BinaryIntOperator, IntExpression):
    operation = "shli",


class IntRightShift(BinaryIntOperator, IntExpression):
    operation = "shri",


# --------------------------
# integer logical operations
# --------------------------


class IntLogicalConjunction(BinaryIntOperator, CharExpression):
    operation = "landi",


class IntLogicalDisjunction(BinaryIntOperator, CharExpression):
    operation = "lori",


class IntLogicalNegation(UnaryIntOperator, IntExpression):
    operation = "lnoti",


# ----------------------------
# integer comparison operators
# ----------------------------


class IntEqualityComparison(BinaryIntOperator, CharExpression):
    operation = "eqi",


class IntInequalityComparison(BinaryIntOperator, CharExpression):
    operation = "neqi",


class IntGreaterThanComparison(BinaryIntOperator, CharExpression):
    operation = "gti",


class IntGreaterThanOrEqualComparison(BinaryIntOperator, CharExpression):
    operation = "gtei",


class IntLessThanComparison(BinaryIntOperator, CharExpression):
    operation = "lti",


class IntLessThanOrEqualComparison(BinaryIntOperator, CharExpression):
    operation = "ltei",


# ----------------------------
# integer conversion operators
# ----------------------------


class IntToCharConversion(UnaryIntOperator, CharExpression):
    operation = "itoc",


class IntToFloatConversion(UnaryIntOperator, FloatExpression):
    operation = "itof",
