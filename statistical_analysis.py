"""
Ентропійний аналіз, тест на стиснення, хі-квадрат, тест Колмогорова-Смірнова, тест Шапіро-Вілка
"""

import bz2
import gzip
import lzma
import statistics
import zlib
from collections import Counter

import mpmath
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


def compression_test(data) -> dict:
    if type(data) in (bytes, bytearray):
        pass
    elif type(data) == str:
        data = data.encode("utf-8")
    else:
        raise TypeError(f"A bytes-like object or string was expected, got {type(data)}")

    zlib_compression = zlib.compress(data)
    gzip_compression = gzip.compress(data)
    bz2_compression = bz2.compress(data)
    lzma_compression = lzma.compress(data)
    zstd_compression = zstd.compress(data)

    results = {
        "zlib": len(zlib_compression) / len(data),
        "gzip": len(gzip_compression) / len(data),
        "bz2": len(bz2_compression) / len(data),
        "lzma": len(lzma_compression) / len(data),
        "zstd": len(zstd_compression) / len(data),
    }

    return statistics.mean(list(results.values()))
