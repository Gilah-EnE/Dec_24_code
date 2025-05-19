import autocorr_test
import signature_analysis
import kolmogorov_test
import primary_analysis
import compression_test
import signature_analysis
import prepare

from pathlib import Path
import sys
import math
import os
import time
from collections import Counter

def create_counter(filename: str, bs: int) -> Counter:
    byte_counts = Counter()
    n = 0
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(bs)
            if not chunk:
                break
            n += len(chunk)
            print(n/1024/1024, end='\r')
            byte_counts += Counter(chunk)
            del chunk
    return filename, n, byte_counts

def main():
    if len(sys.argv) < 1:
        print("Не указано имя файла.")
        sys.exit(1)
    fname = sys.argv[1]

    file_size = os.path.getsize(fname)
    block_size, autocorr_threshold, ks_test_threshold, compression_threshold, signature_threshold, entropy_threshold = 1048576, 0.125, 0.1, 1.1, 150, 7.95

    min_counts = 16
    autocorr_block_size = min(1048576, pow(2, math.floor(math.log2(file_size/min_counts))))

    file_stem, file_extension = os.path.splitext(fname)
    opt_fname = f"{file_stem}_opt{file_extension}"

    if not os.path.exists(opt_fname):
        prepare.optimize_disk_image(fname, 4096)
    
    autocorr_start = time.time()
    autocorr_test.analyze_image_file(fname, autocorr_block_size, False)
    autocorr_end = time.time()
    print("Autocorr: ", autocorr_end - autocorr_start)

    counter_start = time.time()
    counter_fname, n, counter = create_counter(fname, block_size)
    counter_end = time.time()
    print("Counter: ", counter_end - counter_start)

    ks_start = time.time()
    kolmogorov_test.calculate_kolmogorov_smirnov(counter_fname, n, counter, False)
    ks_end = time.time()
    print("K-S: ", ks_end - ks_start)

    cmp_start = time.time()
    compression_test.compression_test(fname)
    cmp_end = time.time()
    print("Compression: ", cmp_end - cmp_start)

    sig_start = time.time()
    signature_analysis.perform_signature_analysis(fname, block_size)
    sig_end = time.time()
    print("Signatures: ", sig_end - sig_start)

    e_start = time.time()
    primary_analysis.entropy_estimation(counter_fname, n, counter)
    e_end = time.time()
    print("Entropy: ", e_end - e_start)
    

if __name__ == "__main__":
    main()