from td4_flet.port import Port
from td4_flet.register import Register
from td4_flet.rom import Rom
from td4_flet.opcode import OpCode


class Cpu:
    def __init__(self) -> None:
        self.pc: int = 0
        self.carry: bool = False
        self.register = Register()
        self.rom = Rom()
        self.port = Port()

    def fetch(self) -> tuple[int, int]:
        memory = self.rom.memory[self.pc]
        opcode = memory >> 4
        operand = memory & 0b1111
        return (opcode, operand)

    def execute(self) -> None:
        (opcode, operand) = self.fetch()
        match opcode:
            case OpCode.AddA:
                self.register.a += operand
                self.carry = self.register.a >> 4 & 1 == 1
                self.register.a &= 0b1111
            case OpCode.AddB:
                self.register.b += operand
                self.carry = self.register.b >> 4 & 1 == 1
                self.register.b &= 0b1111
            case OpCode.MovA:
                self.register.a = operand
                self.carry = False
            case OpCode.MovB:
                self.register.b = operand
                self.carry = False
            case OpCode.MovA2B:
                self.register.a = self.register.b
                self.carry = False
            case OpCode.MovB2A:
                self.register.b = self.register.a
                self.carry = False
            case OpCode.InA:
                self.register.a = self.port.input
                self.carry = False
            case OpCode.InB:
                self.register.b = self.port.input
                self.carry = False
            case OpCode.Out:
                self.port.output = f"{operand:04b}"
                self.carry = False
            case OpCode.OutB:
                self.port.output = f"{self.register.b:04b}"
                self.carry = False
            case OpCode.Jmp:
                self.pc = operand
                self.carry = False
            case OpCode.Jnc:
                if not self.carry:
                    self.pc = operand
                    return
                self.carry = False
            case OpCode.Brk:
                return
            case _:
                raise NotImplementedError("This OpCode not implemented")
        self.pc = (self.pc + 1) & 0b1111
