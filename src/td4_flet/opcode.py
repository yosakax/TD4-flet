class OpCode:
    AddA = 0b0000  # register A + operand
    AddB = 0b0101  # register B + operand
    MovA = 0b0011  # register A <- operand
    MovB = 0b0111  # register B <- operand
    MovA2B = 0b0001  # register A <- register B
    MovB2A = 0b0100  # register B <- register A
    Jmp = 0b1111  # pc <- operand
    Jnc = 0b1110  # if !carry {pc <- operand}
    InA = 0b0010  # register A <- port.input
    InB = 0b0110  # register B <- port.input
    OutB = 0b1001  # port.output <- register B
    Out = 0b1011  # port.output <- operand
    Brk = 0b1101  # ** exit code.
