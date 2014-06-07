# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from functools import wraps


def pops(*types):
    """Decorator that pops len(types) values off the stack, converts them
    either to 'int', 'float' or 'char' and appends them to the function's
    argument list. Only valid for FullCircleVirtualMachine's methods."""
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            args = list(args)
            for conv in types:
                args.append(self.pop(conv))
            return f(self, *args, **kwargs)
        return wrapper
    return decorator


def pushes(type_):
    """Decorator that pushes a function's result on the stack, converting it
    to `type_` (either to 'int', 'float' or 'char'). Only valid for
    FullCircleVirtualMachine's methods."""
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            self.push(result, type_)
        return wrapper
    return decorator
