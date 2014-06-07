# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.tokens.base import Token


class Keyword(Token):
    """The base class for every keyword"""


class AutoKeyword(Keyword):
    """Represents an 'auto' keyword"""


class BreakKeyword(Keyword):
    """Represents a 'break' keyword"""


class ConstKeyword(Keyword):
    """Represents a 'const' keyword"""


class ContinueKeyword(Keyword):
    """Represents a 'continue' keyword"""


class DoKeyword(Keyword):
    """Represents a 'do' keyword"""


class EnumKeyword(Keyword):
    """Represents an 'enum' keyword"""


class ExternKeyword(Keyword):
    """Represents an 'extern' keyword"""


class FloatKeyword(Keyword):
    """Represents a 'float' keyword"""


class DoubleKeyword(Keyword):
    """Represents a 'double' keyword"""


class ForKeyword(Keyword):
    """Represents a 'for' keyword"""


class GotoKeyword(Keyword):
    """Represents a 'goto' keyword"""


class IfKeyword(Keyword):
    """Represents an 'if' keyword"""


class ElseKeyword(Keyword):
    """Represents an 'else' keyword"""


class IntKeyword(Keyword):
    """Represents an 'int' keyword"""


class CharKeyword(Keyword):
    """Represents a 'char' keyword"""


class RegisterKeyword(Keyword):
    """Represents a 'register' keyword"""


class ReturnKeyword(Keyword):
    """Represents a 'return' keyword"""


class ShortKeyword(Keyword):
    """Represents a 'short' keyword"""


class LongKeyword(Keyword):
    """Represents a 'long' keyword"""


class SignedKeyword(Keyword):
    """Represents a 'signed' keyword"""


class UnsignedKeyword(Keyword):
    """Represents an 'unsigned' keyword"""


class SizeofKeyword(Keyword):
    """Represents a 'sizeof' keyword"""


class StaticKeyword(Keyword):
    """Represents a 'static' keyword"""


class StructKeyword(Keyword):
    """Represents a 'struct' keyword"""


class SwitchKeyword(Keyword):
    """Represents a 'switch' keyword"""


class CaseKeyword(Keyword):
    """Represents a 'case' keyword"""


class DefaultKeyword(Keyword):
    """Represents a 'default' keyword"""


class TypedefKeyword(Keyword):
    """Represents a 'typedef' keyword"""


class UnionKeyword(Keyword):
    """Represents a 'union' keyword"""


class VoidKeyword(Keyword):
    """Represents a 'void' keyword"""


class VolatileKeyword(Keyword):
    """Represents a 'volatile' keyword"""


class WhileKeyword(Keyword):
    """Represents a 'while' keyword"""
