# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

from fcc.vm.exceptions import (StackUnderflow, StackOverflow, DivisionByZero,
                               SegmentationFault, ProgramTerminated)
from fcc.vm.decorators import pushes, pops

from struct import pack, unpack


class FullCircleVirtualMachine(object):
    def __init__(self, code):
        """Creates a virtual machine that will execute `code`. `code` must be
        a list of (`instruction`, `arg1`, `arg2`, ...) tuples."""
        self.code = code
        self.sp = self.ip = 0

    def run(self, stack=65536):
        """Starts executing the associated code until the instruction pointer
        reaches the end of the code, or until an error occurs. At most `stack`
        bytes will be available to the program (defaults to 64K). If the code
        terminates gracefully, the stack is returned. Otherwise, a
        `VirtualMachineError` exception is raised."""
        self.start(stack)
        try:
            while True:
                self.step()
        except ProgramTerminated:
            return self.stack
        finally:
            self.stop()

    def start(self, stack=65536):
        """Like `run`, but allows step by step debugging. When the debugging
        session is over, `stop` must be called to release the stack."""
        self.stack = bytearray(stack)
        self.sp = self.ip = 0

    def stop(self):
        """Must be called when using `start` and `step` to free the stack."""
        self.stack = None

    def step(self):
        """Executes the next instruction as determined by `self.ip`. Raises a
        `ProgramTerminated` if the program  On error, raises a
        `VirtualMachineError` exception."""
        if self.ip == len(self.code) or self.stack is None:
            raise ProgramTerminated

        instruction, args = self.code[self.ip][0], self.code[self.ip][1:]
        getattr(self, "_" + instruction)(*args)
        self.ip += 1

    # internal stack manipulation; do not use externally
    def push(self, value, type_=None):
        """Pushes 'value' on the stack. If 'value' is an int, it is represented
        as a 32 bits two's complement integer; otherwise it is stored as a IEEE
        754 single precision floating point number."""
        if type_ is None:
            # autodetect type
            if isinstance(value, float):
                type_ = float
            else:
                type_ = int

        if type_ == float:
            fstring = b"f"
            fsize = 4
        elif type_ == int:
            fstring = b"i"
            fsize = 4
        else:
            fstring = b"B"
            fsize = 1

        self.sp += fsize
        if self.sp > len(self.stack):
            raise StackOverflow

        self.stack[self.sp-fsize:self.sp] = pack(fstring, value)

    def pop(self, type_):
        """Pops a value of type `type` off the stack, returning it as a member
        of the requested type."""
        if type_ == float:
            fstring = b"f"
            fsize = 4
        elif type_ == int:
            fstring = b"i"
            fsize = 4
        else:
            fstring = b"B"
            fsize = 1

        self.sp -= fsize
        if self.sp < 0:
            raise StackUnderflow

        return unpack(fstring, self.stack[self.sp:self.sp+fsize])[0]

    # instruction set; do not use externally

    # stack management
    def _alloc(self, count):
        """Allocates `count` bytes on the stack by moving the stack pointer to
        the right. The block is uninitialized and may contain random data."""
        self.sp += count
        if self.sp > len(self.stack):
            raise StackOverflow

    def _loadi(self, value):
        """Allocates a 32 bit two's complement integer onto the stack, and
        initializes it to `value`. If the stack cannot be expanded, a
        StackOverflow exception is raised."""
        self.push(value)

    def _loadf(self, value):
        """Allocates a single precision IEEE 754 floating point number onto the
        stack, and initializes it to `value`. If the stack cannot be expanded,
        a StackOverflow exception is raised."""
        self.push(value)

    def _loadc(self, value):
        """Allocates a byte onto the stack, and initializes it to `value`. If
        the stack cannot be expanded, a StackOverflow exception is raised."""
        self.push(value)

    def _release(self, count):
        """Releases `count` bytes from the stack by moving the stack pointer to
        the left."""
        self.sp -= count
        if self.sp < 0:
            raise StackUnderflow

    def _pushi(self, addr):
        """Pushes a 32 bit value starting at `addr` onto the stack, and
        increases the stack pointer by 4. If the stack cannot be expanded, a
        StackOverflow exception is raised. If `addr` is negative, or if
        `addr` + 4 lies beyond the stack boundary, a SegmentationFault
        exception is raised."""
        if addr < 0:
            addr += self.sp

        self.sp += 4

        if self.sp > len(self.stack):
            raise StackOverflow

        if addr < 0 or addr > self.sp - 8:
            raise SegmentationFault

        self.stack[self.sp-4:self.sp] = self.stack[addr:addr+4]
    _pushf = _pushi

    def _pushc(self, addr):
        """Pushes the byte at `addr` onto the stack, and increases the stack
        pointer by 1. If the stack cannot be expanded, a StackOverflow
        exception is raised. If `addr` is negative, or if `addr` + 1 lies
        beyond the stack boundary, a SegmentationFault exception is raised."""
        if addr < 0:
            addr += self.sp

        self.sp += 1

        if self.sp > len(self.stack):
            raise StackOverflow

        if addr < 0 or addr > self.sp - 2:
            raise SegmentationFault

        self.stack[self.sp-1] = self.stack[addr]

    def _puship(self):
        """Pushes the instruction pointer onto the stack, and increases the
        stack pointer by 4. If the stack cannot be expanded, a StackOverflow
        exception is raised."""
        self.push(self.ip)

    def _popi(self, addr):
        """Pops a 32 bit value off the stack, stores it at `addr`:`addr`+4 and
        decreases the stack pointer by 4. If the stack cannot be shrunk, a
        StackOverflow exception is raised. If `addr` is negative, or if
        `addr` + 4 ends beyond the stack boundary, a SegmentationFault
        exception is raised."""
        if addr < 0:
            addr += self.sp

        self.sp -= 4
        if self.sp < 0:
            raise StackUnderflow

        if addr < 0 or addr > self.sp - 4:
            raise SegmentationFault

        self.stack[addr:addr+4] = self.stack[self.sp:self.sp+4]
    _popf = _popi

    def _popc(self, addr):
        """Pops a byte value off the stack, stores it at `addr` and decreases
        the stack pointer by 1. If the stack cannot be shrunk, a StackOverflow
        exception is raised. If `addr` is negative, or if `addr` + 1 lies
        beyond the stack boundary, a SegmentationFault exception is raised."""
        if addr < 0:
            addr += self.sp

        self.sp -= 1
        if self.sp < 0:
            raise StackUnderflow

        if addr < 0 or addr > self.sp - 1:
            raise SegmentationFault

        self.stack[addr] = self.stack[self.sp]

    def _popip(self):
        """Pops the instruction pointer from the stack, and decreases the
        stack pointer by 4. If the stack cannot be shrunk, a StackUnderflow
        exception is raised."""
        self.ip = self.pop(int)

    # flow control
    def _nop(self):
        """Does absolutely nothing except move the instruction pointer by one
        (implicit on all instructions)."""

    def _jmp(self, addr):
        """Moves the instruction pointer to `addr`. Raises SegmentationFault
        if `addr` is negative, or outside the program flow."""
        if addr < 0 or addr > len(self.code):
            raise SegmentationFault

        self.ip = addr - 1

    def _jmpr(self, addr):
        """Adds `addr` to the instruction pointer. Raises SegmentationFault
        if the resulting address is negative or outside the program flow."""
        addr += self.ip

        if addr < 0 or addr > len(self.code):
            raise SegmentationFault

        self.ip = addr

    @pops(str)
    def _jmp1(self, addr, flag):
        """Pops an unsigned byte off the stack. If it contains a non-zero bit,
        moves the instruction pointer to `addr`. Raises SegmentationFault if
        `addr` is negative, or outside the program flow."""
        if addr < 0 or addr > len(self.code):
            raise SegmentationFault

        if flag != 0:
            self.ip = addr - 1

    @pops(str)
    def _jmp1r(self, addr, flag):
        """Pops an unsigned byte off the stack. If it contains a non-zero bit,
        adds `addr` to the instruction pointer. Raises SegmentationFault if
        `addr` is negative, or outside the program flow."""
        addr += self.ip

        if addr < 0 or addr > len(self.code):
            raise SegmentationFault

        if flag != 0:
            self.ip = addr

    @pops(str)
    def _jmp0(self, addr, flag):
        """Pops an unsigned byte off the stack. If all of its bits are 0, moves
        the instruction pointer to `addr`. Raises SegmentationFault if `addr`
        is negative, or outside the program flow."""
        if addr < 0 or addr > len(self.code):
            raise SegmentationFault

        if flag == 0:
            self.ip = addr - 1

    @pops(str)
    def _jmp0r(self, addr, flag):
        """Pops an unsigned byte off the stack. If all of its bits are 0, adds
        `addr` to the instruction pointer. Raises SegmentationFault if `addr`
        is negative, or outside the program flow."""
        addr += self.ip

        if addr < 0 or addr > len(self.code):
            raise SegmentationFault

        if flag == 0:
            self.ip = addr

    # output
    @pops(int)
    @pushes(int)
    def _printi(self, a):
        print a
        return a

    @pops(float)
    @pushes(float)
    def _printf(self, a):
        print a
        return a

    @pops(str)
    @pushes(str)
    def _printc(self, a):
        print a
        return a

    # bitwise functions (int and char only)
    @pops(int, int)
    @pushes(int)
    def _bandi(self, a, b):
        return a & b

    @pops(str, str)
    @pushes(str)
    def _bandc(self, a, b):
        return a & b

    @pops(int, int)
    @pushes(int)
    def _bori(self, a, b):
        return a | b

    @pops(str, str)
    @pushes(str)
    def _borc(self, a, b):
        return a | b

    @pops(int, int)
    @pushes(int)
    def _xori(self, a, b):
        return a ^ b

    @pops(str, str)
    @pushes(str)
    def _xorc(self, a, b):
        return a ^ b

    @pops(int)
    @pushes(int)
    def _bnoti(self, a):
        return ~a

    @pops(str)
    @pushes(str)
    def _bnotc(self, a):
        return ~a

    @pops(int, int)
    @pushes(int)
    def _shli(self, b, a):
        return a << b

    @pops(str, str)
    @pushes(str)
    def _shlc(self, b, a):
        return a << b

    @pops(int, int)
    @pushes(int)
    def _shri(self, b, a):
        return a >> b

    @pops(str, str)
    @pushes(str)
    def _shrc(self, b, a):
        return a >> b

    # logical functions
    @pops(int, int)
    @pushes(int)
    def _landi(self, a, b):
        return a and b

    @pops(str, str)
    @pushes(str)
    def _landc(self, a, b):
        return a and b

    @pops(float, float)
    @pushes(float)
    def _landf(self, a, b):
        return a and b

    @pops(int, int)
    @pushes(int)
    def _lori(self, a, b):
        return a or b

    @pops(str, str)
    @pushes(str)
    def _lorc(self, a, b):
        return a or b

    @pops(float, float)
    @pushes(float)
    def _lorf(self, a, b):
        return a or b

    @pops(int)
    @pushes(int)
    def _lnoti(self, a):
        if a:
            return 0
        return 1

    @pops(str)
    @pushes(str)
    def _lnotc(self, a):
        if a:
            return 0
        return 1

    @pops(str)
    @pushes(str)
    def _lnotf(self, a):
        if a:
            return 0
        return 1

    # integer arithmetic
    @pops(int, int)
    @pushes(int)
    def _addi(self, a, b):
        return a + b

    @pops(str, str)
    @pushes(str)
    def _addc(self, a, b):
        return a + b

    @pops(int, int)
    @pushes(int)
    def _subi(self, b, a):
        return a - b

    @pops(str, str)
    @pushes(str)
    def _subc(self, b, a):
        return a - b

    @pops(int, int)
    @pushes(int)
    def _muli(self, a, b):
        return a * b

    @pops(str, str)
    @pushes(str)
    def _mulc(self, a, b):
        return a * b

    @pops(int, int)
    @pushes(int)
    def _divi(self, b, a):
        if b == 0:
            raise DivisionByZero
        return a // b

    @pops(str, str)
    @pushes(str)
    def _divc(self, b, a):
        if b == 0:
            raise DivisionByZero
        return a // b

    @pops(int, int)
    @pushes(int)
    def _modi(self, b, a):
        if b == 0:
            raise DivisionByZero
        return a % b

    @pops(str, str)
    @pushes(str)
    def _modc(self, b, a):
        if b == 0:
            raise DivisionByZero
        return a % b

    @pops(int)
    @pushes(int)
    def _negi(self, a):
        return -a

    @pops(str, str)
    @pushes(str)
    def _negc(self, a):
        return 256 - a

    # floating point math
    @pops(float, float)
    @pushes(float)
    def _addf(self, a, b):
        return a + b

    @pops(float, float)
    @pushes(float)
    def _subf(self, b, a):
        return a - b

    @pops(float, float)
    @pushes(float)
    def _mulf(self, a, b):
        return a * b

    @pops(float, float)
    @pushes(float)
    def _divf(self, b, a):
        return a / b

    @pops(float, float)
    @pushes(float)
    def _pow(self, b, a):
        return a ** b
    _powf = _pow

    # converting between chat, int and float
    @pops(str)
    @pushes(int)
    def _ctoi(self, a):
        return a

    @pops(str)
    @pushes(float)
    def _ctof(self, a):
        return a

    @pops(int)
    @pushes(str)
    def _itoc(self, a):
        return a

    @pops(int)
    @pushes(float)
    def _itof(self, a):
        return a

    @pops(float)
    @pushes(str)
    def _ftoc(self, a):
        return a

    @pops(float)
    @pushes(int)
    def _ftoi(self, a):
        return a

    # comparison functions
    @pops(int, int)
    @pushes(str)
    def _eqi(self, a, b):
        return 1 if a == b else 0
    _eqf = _eqi

    @pops(str, str)
    @pushes(str)
    def _eqc(self, a, b):
        return 1 if a == b else 0

    @pops(int, int)
    @pushes(str)
    def _neqi(self, a, b):
        return 1 if a != b else 0
    _neqf = _neqi

    @pops(str, str)
    @pushes(str)
    def _neqc(self, a, b):
        return 1 if a != b else 0

    @pops(int, int)
    @pushes(str)
    def _gti(self, b, a):
        return 1 if a > b else 0

    @pops(float, float)
    @pushes(str)
    def _gtf(self, b, a):
        return 1 if a > b else 0

    @pops(str, str)
    @pushes(str)
    def _gtc(self, b, a):
        return 1 if a > b else 0

    @pops(int, int)
    @pushes(str)
    def _gtei(self, b, a):
        return 1 if a >= b else 0

    @pops(float, float)
    @pushes(str)
    def _gtef(self, b, a):
        return 1 if a >= b else 0

    @pops(str, str)
    @pushes(str)
    def _gtec(self, b, a):
        return 1 if a >= b else 0

    @pops(int, int)
    @pushes(str)
    def _lti(self, b, a):
        return 1 if a < b else 0

    @pops(float, float)
    @pushes(str)
    def _ltf(self, b, a):
        return 1 if a < b else 0

    @pops(str, str)
    @pushes(str)
    def _ltc(self, b, a):
        return 1 if a < b else 0

    @pops(int, int)
    @pushes(str)
    def _ltei(self, b, a):
        return 1 if a <= b else 0

    @pops(float, float)
    @pushes(str)
    def _ltef(self, b, a):
        return 1 if a <= b else 0

    @pops(str, str)
    @pushes(str)
    def _ltec(self, b, a):
        return 1 if a <= b else 0
