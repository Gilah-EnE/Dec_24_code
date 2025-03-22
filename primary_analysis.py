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


def entropy_estimation(filename, bs=1048576):
    with open(filename, 'rb') as file:
        n = 0
        byte_counts = Counter("")
        while True:
            chunk = file.read(bs)
            if not chunk:
                break

            n += len(chunk)
            print(n / (1024 * 1024), end="\r", flush=True)
            byte_counts += Counter(chunk)
            del chunk

    entropy = mpmath.mpf(0)

    for count in byte_counts.values():
        p = mpmath.fdiv(count, n)
        entropy = mpmath.fadd(entropy, mpmath.fmul(p, mpmath.log(p, 2)))

    print("\n", filename, -entropy)

entropy_estimation("/dataset/images/random_1M.img")
