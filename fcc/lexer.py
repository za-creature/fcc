# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc import tokens

from string import whitespace


class FullCircleLexer(object):
    tokens = [
        ("unsigned", tokens.UnsignedKeyword),
        ("volatile", tokens.VolatileKeyword),
        ("register", tokens.RegisterKeyword),
        ("continue", tokens.ContinueKeyword),
        ("default", tokens.DefaultKeyword),
        ("typedef", tokens.TypedefKeyword),
        ("double", tokens.DoubleKeyword),
        ("extern", tokens.ExternKeyword),
        ("struct", tokens.StructKeyword),
        ("static", tokens.StaticKeyword),
        ("switch", tokens.SwitchKeyword),
        ("return", tokens.ReturnKeyword),
        ("sizeof", tokens.SizeofKeyword),
        ("signed", tokens.SignedKeyword),
        ("break", tokens.BreakKeyword),
        ("const", tokens.ConstKeyword),
        ("float", tokens.FloatKeyword),
        ("short", tokens.ShortKeyword),
        ("union", tokens.UnionKeyword),
        ("while", tokens.WhileKeyword),
        ("auto", tokens.AutoKeyword),
        ("case", tokens.CaseKeyword),
        ("char", tokens.CharKeyword),
        ("else", tokens.ElseKeyword),
        ("enum", tokens.EnumKeyword),
        ("goto", tokens.GotoKeyword),
        ("long", tokens.LongKeyword),
        ("void", tokens.VoidKeyword),
        ("for", tokens.ForKeyword),
        ("int", tokens.IntKeyword),
        ("<<=", tokens.LeftShiftAssignmentOperator),
        (">>=", tokens.RightShiftAssignmentOperator),
        ("do", tokens.DoKeyword),
        ("if", tokens.IfKeyword),
        ("++", tokens.IncrementOperator),
        ("--", tokens.DecrementOperator),
        ("<<", tokens.LeftShiftOperator),
        (">>", tokens.RightShiftOperator),
        ("==", tokens.EqualityOperator),
        ("!=", tokens.InequalityOperator),
        (">=", tokens.GreaterThanOrEqualOperator),
        ("<=", tokens.LessThanOrEqualOperator),
        ("&&", tokens.LogicalConjunctionOperator),
        ("||", tokens.LogicalDisjunctionOperator),
        ("+=", tokens.AdditionAssignmentOperator),
        ("-=", tokens.SubstractionAssignmentOperator),
        ("*=", tokens.MultiplicationAssignmentOperator),
        ("/=", tokens.DivisionAssignmentOperator),
        ("%=", tokens.ModulusAssignmentOperator),
        ("&=", tokens.BitwiseConjunctionAssignmentOperator),
        ("|=", tokens.BitwiseDisjunctionAssignmentOperator),
        ("^=", tokens.ExclusiveDisjunctionAssignmentOperator),
        ("->", tokens.StructureDereferenceOperator),
        ("+", tokens.AdditionOperator),
        ("-", tokens.SubstractionOperator),
        ("*", tokens.MultiplicationOperator),
        ("/", tokens.DivisionOperator),
        ("%", tokens.ModulusOperator),
        ("=", tokens.AssignmentOperator),
        ("&", tokens.BitwiseConjunctionOperator),
        ("|", tokens.BitwiseDisjunctionOperator),
        ("^", tokens.ExclusiveDisjunctionOperator),
        ("~", tokens.BitwiseNegationOperator),
        ("[", tokens.ArraySubscriptStartOperator),
        ("]", tokens.ArraySubscriptEndOperator),
        (".", tokens.StructureReferenceOperator),
        (">", tokens.GreaterThanOperator),
        ("<", tokens.LessThanOperator),
        ("`", tokens.FullCircleBacktickOperator),
        ("!", tokens.LogicalNegationOperator),
        ("{", tokens.BlockStartToken),
        ("}", tokens.BlockEndToken),
        ("(", tokens.OpenParanthesisOperator),
        (")", tokens.CloseParanthesisOperator),
        (",", tokens.CommaOperator),
        (";", tokens.SemicolonToken)
    ]

    def __init__(self, data):
        self.data = data
        self.position = 0
        self.line = self.column = 1
        self.limit = len(data)

    def lex(self):
        """Parses `self.data` and returns an array of tokens. Raises an
        exception on error."""
        result = []
        while self.position < self.limit:
            if self.data.startswith("//", self.position):
                # inline comment
                self.skip_inline_comment()
            elif self.data.startswith("/*", self.position):
                # multiline comment
                self.skip_multiline_comment()
            else:
                for token, cls in self.tokens:
                    # check for static tokens
                    if self.data.startswith(token, self.position):
                        # static token found; add and advance
                        result.append(cls(self.line, self.column))
                        self.position += len(token)
                        self.column += len(token)
                        break
                else:
                    # no static tokens begin at this position

                    if self.data[self.position] in "\r\n":
                        # newline
                        self.skip_newline()
                    elif self.data[self.position] in whitespace:
                        # non-newline whitespace
                        self.skip_whitespace()
                    elif self.data[self.position] in "0123456789.":
                        # numeric constant
                        result.append(self.parse_numeric_constant())
                    elif self.data[self.position] in "'\"":
                        # string or character constant
                        result.append(self.parse_string_constant())
                    elif self.data[self.position].lower() in \
                            "_abcdefghijklmnopqrstuvwxyz":
                        # identifier
                        result.append(self.parse_identifier())
                    else:
                        raise ValueError("Unexpected symbol")
        return result

    def skip_inline_comment(self):
        """Skip characters until the end of the line"""
        while self.data[self.position] not in "\r\n":
            self.skip_whitespace()
            if self.position == self.limit:
                break  # reached EOF
        else:
            self.skip_newline()

    def skip_multiline_comment(self):
        """Skip characters until */ is found."""
        while not self.data.startswith("*/", self.position):
            if self.data[self.position] in "\r\n":
                self.skip_newline()
            else:
                self.skip_whitespace()

            if self.position == self.limit:
                break  # reached EOF
        else:
            self.skip_whitespace()
            self.skip_whitespace()

    def skip_newline(self):
        self.line += 1
        self.column = 1
        self.position += 1

    def skip_whitespace(self):
        self.column += 1
        self.position += 1

    def parse_numeric_constant(self):
        value = ""

        while self.data[self.position].lower() in "0123456789abcdefx.":
            value += self.data[self.position].lower()
            self.skip_whitespace()

            if self.position == self.limit:
                break  # reached EOF

        if \
                "." in value or \
                (value[-1] in "fd" and not value.startswith("0x")):
            # value is explicit floating point
            if value[-1] in "fd":
                value = value[:-1]
            return tokens.FloatConstant(float(value), self.line, self.column)

        # value must be an integer
        base = 10
        if value[0] == "0":
            if "x" in value:
                base = 16
            else:
                base = 8
        return tokens.IntConstant(int(value, base), self.line, self.column)

    def parse_string_constant(self):
        value = ""
        delimiter = self.data[self.position]
        self.skip_whitespace()
        if self.position == self.limit:
            raise ValueError("Unexpected end of file")

        while self.data[self.position].lower() != delimiter:
            if self.data[self.position] == "\\":
                # escape code encountered; read next char to disambiguate
                self.skip_whitespace()
                if self.position == self.limit:
                    # EOF reached without string terminator
                    raise ValueError("Unexpected end of file")

                if self.data[self.position] in "\r\n":
                    # escaped newline; ignore both characters
                    self.skip_newline()
                else:
                    # add entire escape sequence to string
                    value += "\\" + self.data[self.position]
                    self.skip_whitespace()
            else:
                value += self.data[self.position].lower()
                self.skip_whitespace()

            if self.position == self.limit:
                # EOF reached without string terminator
                raise ValueError("Unexpected end of file")
        self.skip_whitespace()

        return tokens.CharConstant(value.decode("string_escape"), self.line,
                                   self.column)

    def parse_identifier(self):
        value = ""
        while self.data[self.position].lower() in \
                "_abcdefghijklmnopqrstuvwxyz0123456789":
            value += self.data[self.position]

            self.skip_whitespace()
            if self.position == self.limit:
                break

        return tokens.Identifier(value, self.line, self.column)
