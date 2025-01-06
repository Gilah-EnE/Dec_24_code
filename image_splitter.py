from pygpt.gpt_file import GPTFile
from pygpt.partition_table_header import PartitionTableHeader

import os


class GPTReader(object):
    def __init__(self, filename, sector_size=512, little_endian=True):
        self._filename = filename
        self._sector_size = sector_size
        self._file = GPTFile(filename, sector_size)
        self._pth = PartitionTableHeader(self._file, little_endian)

    @property
    def partition_table(self):
        return self._pth

    @property
    def block_reader(self):
        return self._file


def split_image(fname: str, sector_size=512, dry_run=True) -> list:
    reader = GPTReader(fname, sector_size=sector_size)
    files = list()

    if len(list(reader.partition_table.valid_entries())) == 0:
        raise ValueError("No valid partitions found")

    for partition in reader.partition_table.valid_entries():
        file_base_name = partition.partition_id

        out_file = os.path.join(os.getcwd(), f"{file_base_name}.bin")
        files.append(out_file)

        if not dry_run:
            with open(out_file, "wb+") as fout:
                for block in reader.block_reader.blocks_in_range(
                    partition.first_block, partition.length
                ):
                    fout.write(block)

    return files
