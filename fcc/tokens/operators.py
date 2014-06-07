# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.tokens.base import Token

# ----
# base
# ----


class Operator(Token):
    """The base class for every operator"""


class UnaryOperator(Operator):
    """Base class for operators known to be unary only."""


class BinaryOperator(Operator):
    """Base class for operators known to be binary only."""


class AssignmentOperator(BinaryOperator):
    """Represents the '=' assignment operator. It is also the base class for
    the compound assignment operators (such as +=)."""


# ----------
# arithmetic
# ----------


class AdditionOperator(BinaryOperator):
    """Represents the '+' addition operator"""


class SubstractionOperator(BinaryOperator):
    """Represents the '-' substraction operator"""


class MultiplicationOperator(BinaryOperator):
    """Represents the '*' multiplication operator"""


class DivisionOperator(BinaryOperator):
    """Represents the '/' division operator"""


class ModulusOperator(BinaryOperator):
    """Represents the '%' modulus operator"""


class IncrementOperator(UnaryOperator):
    """Represents the '++' increment operator"""


class DecrementOperator(UnaryOperator):
    """Represents the '++' increment operator"""


# -------
# bitwise
# -------


class BitwiseConjunctionOperator(BinaryOperator):
    """Represents the '&' bitwise conjunction operator"""


class BitwiseDisjunctionOperator(BinaryOperator):
    """Represents the '|' bitwise disjunction operator"""


class ExclusiveDisjunctionOperator(BinaryOperator):
    """Represents the '^' bitwise exclusive disjunction operator"""


class LeftShiftOperator(BinaryOperator):
    """Represents the '<<' left shift operator"""


class RightShiftOperator(BinaryOperator):
    """Represents the '>>' right shift operator"""


class BitwiseNegationOperator(UnaryOperator):
    """Represents the '~' bitwise negation operator"""


# ----------
# comparison
# ----------


class EqualityOperator(BinaryOperator):
    """Represents the '==' equality operator"""


class InequalityOperator(BinaryOperator):
    """Represents the '!=' inequality operator"""


class GreaterThanOperator(BinaryOperator):
    """Represents the '>' comparison operator"""


class GreaterThanOrEqualOperator(BinaryOperator):
    """Represents the '>=' comparison operator"""


class LessThanOperator(BinaryOperator):
    """Represents the '<' comparison operator"""


class LessThanOrEqualOperator(BinaryOperator):
    """Represents the '<=' comparison operator"""


# -------
# logical
# -------


class LogicalConjunctionOperator(BinaryOperator):
    """Represents the '&&' logical conjunction operator"""


class LogicalDisjunctionOperator(BinaryOperator):
    """Represents the '||' logical disjunction operator"""


class LogicalNegationOperator(UnaryOperator):
    """Represents the '!' logical negation operator"""


# --------
# compound
# --------


class AdditionAssignmentOperator(AssignmentOperator):
    """Represents the '+=' addition assignment operator"""


class SubstractionAssignmentOperator(AssignmentOperator):
    """Represents the '-=' substraction assignment operator"""


class MultiplicationAssignmentOperator(AssignmentOperator):
    """Represents the '*=' multiplication assignment operator"""


class DivisionAssignmentOperator(AssignmentOperator):
    """Represents the '/=' division assignment operator"""


class ModulusAssignmentOperator(AssignmentOperator):
    """Represents the '%=' modulus assignment operator"""


class BitwiseConjunctionAssignmentOperator(AssignmentOperator):
    """Represents the '&=' bitwise conjunction assignment operator"""


class BitwiseDisjunctionAssignmentOperator(AssignmentOperator):
    """Represents the '|=' bitwise disjunction assignment operator"""


class ExclusiveDisjunctionAssignmentOperator(AssignmentOperator):
    """Represents the '^=' bitwise exclusive disjunction assignment operator"""


class LeftShiftAssignmentOperator(AssignmentOperator):
    """Represents the '<<=' left shift assignment operator"""


class RightShiftAssignmentOperator(AssignmentOperator):
    """Represents the '>>=' right shift assignment operator"""


# ---------
# structure
# ---------


class ArraySubscriptStartOperator(Operator):
    """Represents the '[' array subscript start operator"""


class ArraySubscriptEndOperator(Operator):
    """Represents the ']' array subscript end operator"""


class StructureDereferenceOperator(Operator):
    """Represents the '->' structure dereference operator"""


class StructureReferenceOperator(Operator):
    """Represents the '.' structure reference operator"""


class OpenParanthesisOperator(Operator):
    """Represents the '(' open paranthesis"""


class CloseParanthesisOperator(Operator):
    """Represents the ')' closed paranthesis"""


class CommaOperator(BinaryOperator):
    """Represents the ',' comma token"""


class FunctionApplicationOperator(Operator):
    """Dummy class used by the parser."""


class AdditiveNegationOperator(Operator):
    """Used by the parser to represent -x"""


class FullCircleBacktickOperator(UnaryOperator):
    """Represents the '`' print and return operator (fcc extension)."""