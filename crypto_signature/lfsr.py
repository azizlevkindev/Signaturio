class LFSR:
    LENGTH = 32
    TAPS = [32, 22, 2, 1]
    
    def __init__(self, initial_state: int):
        self.state = initial_state & 0xFFFFFFFF
    
    def step(self, counter: int, lcg_influence: int = 0) -> int:
        feedback = 0
        for tap in self.TAPS:
            feedback ^= (self.state >> (tap - 1)) & 1
        feedback ^= (lcg_influence >> 16) & 1
        self.state = ((self.state << 1) | feedback) & 0xFFFFFFFF
        if counter % 5 == 0:
            self.state ^= self.state >> 16
            self.state ^= (self.state << 13) & 0xFFFFFFFF
            self.state ^= self.state >> 7
            self.state &= 0xFFFFFFFF
        return self.state
    
    def get_state(self) -> int:
        return self.state
    
    def set_state(self, state: int):
        self.state = state & 0xFFFFFFFF
