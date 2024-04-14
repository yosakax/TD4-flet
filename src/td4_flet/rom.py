class Rom:
    def __init__(self) -> None:
        self.memory = [0] * 16

    def load_bin(self, lines: list[str]):
        for addr, line in enumerate(lines):
            self.memory[addr] = int(line, 2)
