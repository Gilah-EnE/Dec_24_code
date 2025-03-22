import os
import subprocess
import time

from line_profiler_pycharm import profile


@profile
def compression_test(filename: str) -> str:
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        print("Starting test", end="\r")

        gzip_compression = filesize / int(
            subprocess.check_output(f"pigz < {filename} | wc -c", shell=True).decode())
        print("GZip", end=" ")

        lz4_compression = filesize / int(
            subprocess.check_output(f"lz4 < {filename} | wc -c", shell=True).decode())
        print("LZ4", end=" ")

        bz2_compression = filesize / int(
            subprocess.check_output(f"lbzip2 < {filename} | wc -c", shell=True).decode())
        print("Bzip2", end=" ")

        zstd_compression = filesize / int(
            subprocess.check_output(f"zstd -T12 < {filename} | wc -c", shell=True).decode())
        print("Zstd", end=" ")

        xz_compression = filesize / int(
            subprocess.check_output(f"pixz < {filename} | wc -c", shell=True).decode())
        print("XZ", end=" ")

    return f"\r{filename.split("/")[-1]} {gzip_compression} {lz4_compression} {bz2_compression} {zstd_compression} {xz_compression}"


start = time.time()
print(compression_test('/dataset/images/random.img'))
print(compression_test('/dataset/images/kagura/kagura_data_dec.img'))
print(compression_test('/dataset/images/kagura/kagura_data_dec_opt.img'))
print(compression_test('/dataset/images/kagura/kagura_data_enc.img'))
print(compression_test('/dataset/images/kagura/kagura_data_enc_opt.img'))
print(compression_test('/dataset/images/vince/vince_data.img'))
print(compression_test('/dataset/images/vince/vince_data_opt.img'))
print(compression_test('/dataset/images/wd400.img'))
print(compression_test('/dataset/images/wd400_opt.img'))
print(compression_test('/dataset/images/miatoll/miatoll_data_fbe.img'))
print(compression_test('/dataset/images/miatoll/miatoll_data_fbe_opt.img'))
print(compression_test('/dataset/images/miatoll/miatoll_data_nonfbe.img'))
print(compression_test('/dataset/images/miatoll/miatoll_data_nonfbe_opt.img'))
print(compression_test('/dataset/images/adoptable.img'))
print(compression_test('/dataset/images/adoptable_opt.img'))
end = time.time()
print(end - start)
