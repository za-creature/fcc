# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.ast.operators.base import (UnaryOperator, BinaryOperator,
                                    AssignmentOperator)
from fcc.ast.expressions import CharExpression, IntExpression, FloatExpression

# ------------------------
# floating point operators
# ------------------------


class UnaryFloatOperator(UnaryOperator):
    """An unary float operator must have exactly one child, and that child
    must be a float expression."""
    operand_type = FloatExpression


class BinaryFloatOperator(BinaryOperator):
    """A binary float operator must have exactly two children, and those
    children must be float expressions."""
    operand_type = FloatExpression


class FloatAssignment(AssignmentOperator, FloatExpression):
    operand_type = FloatExpression


class FloatBacktick(UnaryFloatOperator, FloatExpression):
    operation = "printf",


# -------------------------
# floating point arithmetic
# -------------------------


class FloatAddition(BinaryFloatOperator, FloatExpression):
    operation = "addf",


class FloatSubstraction(BinaryFloatOperator, FloatExpression):
    operation = "subf",


class FloatMultiplication(BinaryFloatOperator, FloatExpression):
    operation = "mulf",


class FloatDivision(BinaryFloatOperator, FloatExpression):
    operation = "divf",


class FloatExponentiation(BinaryFloatOperator, FloatExpression):
    operation = "powf",


class FloatAdditiveNegation(UnaryFloatOperator, FloatExpression):
    operation = "negf",


# ---------------------------------
# floating point logical operations
# ---------------------------------


class FloatLogicalConjunction(BinaryFloatOperator, CharExpression):
    operation = "landf",


class FloatLogicalDisjunction(BinaryFloatOperator, CharExpression):
    operation = "lorf",


class FloatLogicalNegation(UnaryFloatOperator, IntExpression):
    operation = "lnotf",


# -----------------------------------
# floating point comparison operators
# -----------------------------------


class FloatEqualityComparison(BinaryFloatOperator, CharExpression):
    operation = "eqf",


class FloatInequalityComparison(BinaryFloatOperator, CharExpression):
    operation = "neqf",


class FloatGreaterThanComparison(BinaryFloatOperator, CharExpression):
    operation = "gtf",


class FloatGreaterThanOrEqualComparison(BinaryFloatOperator, CharExpression):
    operation = "gtef",


class FloatLessThanComparison(BinaryFloatOperator, CharExpression):
    operation = "ltf",


class FloatLessThanOrEqualComparison(BinaryFloatOperator, CharExpression):
    operation = "ltef",


# -----------------------------------
# floating point conversion operators
# -----------------------------------


class FloatToCharConversion(UnaryFloatOperator, CharExpression):
    operation = "ftoc",


class FloatToIntConversion(UnaryFloatOperator, IntExpression):
    operation = "ftoi",
