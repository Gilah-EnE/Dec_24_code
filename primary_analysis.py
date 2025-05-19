from concurrent.futures.process import ProcessPoolExecutor

import mpmath
import parted
from collections import Counter
from typing import List


def parted_check(filename: str) -> List[str]:
    found_types = list()
    try:
        device = parted.getDevice(filename)
        disk = parted.newDisk(device)

        for partition in disk.partitions:
            found_types.append(partition.fileSystem.type)

        return [filename, found_types]
    except Exception as ex:
        return [filename, ex]


def entropy_estimation(filename: str, n: int, byte_counts: Counter):
    entropy = mpmath.mpf(0)

    for count in byte_counts.values():
        p = mpmath.fdiv(count, n)
        entropy = mpmath.fadd(entropy, mpmath.fmul(p, mpmath.log(p, 2)))

    return filename, -entropy
