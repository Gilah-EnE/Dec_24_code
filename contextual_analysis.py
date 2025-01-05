import sys
from collections import Counter

import mpmath
from scipy.special import gammaincc


def monobit_test(data) -> bool:
    if type(data) in (bytes, bytearray):
        pass
    elif type(data) == str:
        data = data.encode("utf-8")
    else:
        raise TypeError(f"A bytes-like object or string was expected, got {type(data)}")

    bin_data = bin(int.from_bytes(data, byteorder=sys.byteorder))[2:]
    counter = Counter(list(bin_data))
    count = mpmath.fabs(counter["0"] - counter["1"])
    s_obs = mpmath.fdiv(count, mpmath.sqrt(len(bin_data)))
    p_val = mpmath.erfc(mpmath.fdiv(mpmath.fabs(s_obs) / mpmath.sqrt(2)))
    if p_val < 0.01:
        return False
    else:
        return True


def block_freq_test(data, M: int) -> bool:
    if type(data) in (bytes, bytearray):
        pass
    elif type(data) == str:
        data = data.encode("utf-8")
    else:
        raise TypeError(f"A bytes-like object or string was expected, got {type(data)}")

    bin_data = bin(int.from_bytes(data, byteorder=sys.byteorder))[2:]
    blocks = [bin_data[i : i + M] for i in range(0, len(bin_data), M)]
    if len(blocks[-1]) != M:
        blocks.pop()
    pi = list()
    for block in blocks:
        pi.append(Counter(block)["1"] / M)
    pi_i_sum = 0
    for pi_i in pi:
        pi_i_sum += (pi_i - 0.5) ** 2
    chi_sq_obs = 4 * M * pi_i_sum
    p_val = gammaincc(len(blocks) / 2, chi_sq_obs / 2)
    if p_val < 0.01:
        return False
    else:
        return True
