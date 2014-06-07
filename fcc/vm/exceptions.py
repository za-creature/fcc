# coding=utf-8
from __future__ import absolute_import, unicode_literals, division


class VirtualMachineError(Exception):
    """Base class for all virtual machine errors."""


class StackUnderflow(VirtualMachineError):
    """Raised when an attempt is made to release more memory than allocated."""


class StackOverflow(VirtualMachineError):
    """Raised when an attempt is made to allocate more stack memory than the
    set execution limit."""


class DivisionByZero(VirtualMachineError):
    """Raised when a program attempts to divide by 0."""


class SegmentationFault(VirtualMachineError):
    """Raised when a program attempts to access memory that has not been
    allocated."""


class ProgramTerminated(Exception):
    """Raised by `FullCircleVirtualMachine.step` when the program has
    terminated."""
