import os
import subprocess
import time

def compression_test(filename: str) -> str:
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        # print("Starting test", end="\r")

        gzip_compression = filesize / int(
            subprocess.check_output(f"pigz < {filename} | wc -c", shell=True).decode())
        # print("GZip", end=" ")

        lz4_compression = filesize / int(
            subprocess.check_output(f"lz4 < {filename} | wc -c", shell=True).decode())
        # print("LZ4", end=" ")

        bz2_compression = filesize / int(
            subprocess.check_output(f"lbzip2 < {filename} | wc -c", shell=True).decode())
        # print("Bzip2", end=" ")

        zstd_compression = filesize / int(
            subprocess.check_output(f"zstd -T12 < {filename} | wc -c", shell=True).decode())
        # print("Zstd", end=" ")

        xz_compression = filesize / int(
            subprocess.check_output(f"pixz < {filename} | wc -c", shell=True).decode())
        # print("XZ", end=" ")

    return f"\r{filename.split("/")[-1]} {gzip_compression} {lz4_compression} {bz2_compression} {zstd_compression} {xz_compression}"
