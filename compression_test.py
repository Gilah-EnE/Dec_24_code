import bz2
import gzip
import lzma
import statistics
import zlib
from collections import Counter

import mpmath
import zstandard as zstd


def compression_test(filename) -> dict:
    with open(filename, 'rb') as file:
        data = file.read()

        zlib_compression = zlib.compress(data)
        gzip_compression = gzip.compress(data)
        bz2_compression  = bz2.compress(data)
        lzma_compression = lzma.compress(data)
        zstd_compression = zstd.compress(data)

    results = {
        "zlib": len(zlib_compression) / len(data),
        "gzip": len(gzip_compression) / len(data),
        "bz2":  len(bz2_compression)  / len(data),
        "lzma": len(lzma_compression) / len(data),
        "zstd": len(zstd_compression) / len(data),
    }

    return statistics.mean(list(results.values()))
