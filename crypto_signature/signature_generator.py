from .lcg import LCG
from .lfsr import LFSR
from .initialization import initialize_lcg, initialize_lfsr, apply_initial_coupling


class CryptoSignatureGenerator:
    def __init__(self, timestamp: int = None):
        import time
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        self.timestamp = timestamp
        self.counter = 0
        lcg_state = initialize_lcg(timestamp)
        lfsr_state = initialize_lfsr(timestamp)
        lcg_state, lfsr_state = apply_initial_coupling(lcg_state, lfsr_state)
        self.lcg = LCG(lcg_state)
        self.lfsr = LFSR(lfsr_state)
        self._warmup()
    
    def _warmup(self):
        for _ in range(32):
            lfsr_state = self.lfsr.get_state()
            self.lcg.step(self.counter, lfsr_state)
            lcg_state = self.lcg.get_state()
            self.lfsr.step(self.counter, lcg_state)
    
    def _lcg_step(self) -> int:
        lfsr_state = self.lfsr.get_state()
        return self.lcg.step(self.counter, lfsr_state)
    
    def _lfsr_step(self) -> int:
        lcg_state = self.lcg.get_state()
        return self.lfsr.step(self.counter, lcg_state)
    
    def _nonlinear_mixing(self, value: int) -> int:
        x = value ^ self.timestamp
        x &= 0xFFFFFFFFFFFFFFFF
        for _ in range(3):
            x = (x ^ (x << 13)) & 0xFFFFFFFFFFFFFFFF
            x = (x ^ (x >> 7)) & 0xFFFFFFFFFFFFFFFF
            x = (x ^ (x << 17)) & 0xFFFFFFFFFFFFFFFF
            x = (x ^ (x >> 15)) & 0xFFFFFFFFFFFFFFFF
        return x
    
    def _byte_permutation(self, value: int) -> int:
        bytes_list = [(value >> (i * 8)) & 0xFF for i in range(8)]
        perm = [2, 5, 0, 7, 1, 4, 3, 6]
        permuted = [bytes_list[perm[i]] for i in range(8)]
        result = sum(byte << (i * 8) for i, byte in enumerate(permuted))
        return result & 0xFFFFFFFFFFFFFFFF
    
    def generate_signature(self) -> str:
        lcg_val = self._lcg_step()
        lfsr_val = self._lfsr_step()
        lfsr_48 = (lfsr_val << 16) | (lfsr_val & 0xFFFF)
        lfsr_48 &= (1 << 48) - 1
        rotate = (self.counter * 7) % 48
        rotated_lcg = ((lcg_val << rotate) | (lcg_val >> (48 - rotate))) & ((1 << 48) - 1)
        combined = (rotated_lcg ^ lfsr_48) ^ self.counter
        combined ^= (self.timestamp & 0xFFFFFF)
        combined &= (1 << 48) - 1
        signature_64 = (combined << 16) | (combined & 0xFFFF)
        signature_64 &= 0xFFFFFFFFFFFFFFFF
        signature_64 = self._nonlinear_mixing(signature_64)
        result = self._byte_permutation(signature_64)
        self.counter = (self.counter + (lcg_val & 0xFF) + (lfsr_val & 0xFF)) & 0xFF
        return hex(result)[2:].zfill(16)
    
    def reset(self, timestamp: int = None):
        import time
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        self.timestamp = timestamp
        self.counter = 0
        lcg_state = initialize_lcg(timestamp)
        lfsr_state = initialize_lfsr(timestamp)
        lcg_state, lfsr_state = apply_initial_coupling(lcg_state, lfsr_state)
        self.lcg.set_state(lcg_state)
        self.lfsr.set_state(lfsr_state)
        self._warmup()
