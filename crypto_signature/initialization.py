import hashlib


def initialize_lcg(timestamp: int) -> int:
    hash1 = hashlib.md5(str(timestamp).encode()).digest()
    hash2 = hashlib.md5(hash1 + str(timestamp % 1000).encode()).digest()
    lcg_state = int.from_bytes(hash2[:6], byteorder='big')
    lcg_state &= (1 << 48) - 1
    return lcg_state


def initialize_lfsr(timestamp: int) -> int:
    state = timestamp & 0xFFFFFFFF
    for i in range(32):
        bit = (state ^ (state >> 2) ^ (state >> 3) ^ (state >> 5) ^ (i & 1)) & 1
        state = (state >> 1) | (bit << 31)
    return state & 0xFFFFFFFF


def apply_initial_coupling(lcg_state: int, lfsr_state: int) -> tuple[int, int]:
    lcg_state ^= lfsr_state & 0xFFFFFF
    lcg_state &= (1 << 48) - 1
    lfsr_state ^= lcg_state & 0xFFFFFFFF
    lfsr_state &= 0xFFFFFFFF
    return lcg_state, lfsr_state
