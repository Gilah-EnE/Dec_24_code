import bz2
import gzip
import lzma
import mpmath
import statistics
import zlib
from collections import Counter

import zstandard as zstd


def entropy_estimation(data) -> float:
    if type(data) in (bytes, bytearray):
        pass
    elif type(data) == str:
        data = data.encode("utf-8")
    else:
        raise TypeError(f"A bytes-like object or string was expected, got {type(data)}")

    byte_counts = Counter(data)
    total_bytes = len(data)
    entropy = mpmath.mpf(0)

    for count in byte_counts.values():
        p = mpmath.fdiv(count, total_bytes)
        entropy = mpmath.fadd(entropy, mpmath.fmul(p, mpmath.log2(p)))

    return -entropy


def segment_entropy(data, segsize: int) -> list:
    if type(data) in (bytes, bytearray):
        pass
    elif type(data) == str:
        data = data.encode("utf-8")
    else:
        raise TypeError(f"A bytes-like object or string was expected, got {type(data)}")
    segements = [data[i : i + segsize] for i in range(0, len(data), segsize)]
    segments_entropy = []
    for segment in segements:
        segments_entropy.append(entropy_calc(segment))

    return segments_entropy
