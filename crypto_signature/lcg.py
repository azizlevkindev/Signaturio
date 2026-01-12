class LCG:
    MULTIPLIER = 0x5DEECE66D
    INCREMENT = 0xB
    MODULUS = (1 << 48) - 1
    
    def __init__(self, initial_state: int):
        self.state = initial_state & self.MODULUS
    
    def step(self, counter: int, lfsr_influence: int = 0) -> int:
        extra = (lfsr_influence & 0xFF) if (counter % 3 == 0) else 0
        self.state = (self.MULTIPLIER * (self.state ^ extra) + self.INCREMENT) & self.MODULUS
        return self.state
    
    def get_state(self) -> int:
        return self.state
    
    def set_state(self, state: int):
        self.state = state & self.MODULUS
