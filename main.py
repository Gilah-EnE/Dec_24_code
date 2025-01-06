import autocorr_test
import signature_analysis
import kolmogorov_test
import nist_sts
import pearson_criterion
import primary_analysis
import statistical_analysis
import signature_analysis
import image_splitter

from pathlib import Path
import sys

def run_tests(partition_path):
    try:
        print("Autocorrelation test started")
        autocorr_value = autocorr_test.analyze_image_file(partition_path, False)
        autocorr_verdict =  autocorr_value >= 0.05
        print(f"Autocorr result: {autocorr_value} ({autocorr_verdict})")
    except Exception as e:
        print(f"Autocorrelation test failed: {e}")
        autocorr_verdict = True

def main():
    print("---PARTITION ENCRYPTION FINDER PROTOTYPE---")

    try:
        filename = "/home/gilah/Documents/test_gpt.bin"  # input("Enter path to the file: ")
        if not Path(filename).exists():
            raise FileNotFoundError
    except FileNotFoundError as e:
        print(f"Error: File {filename} not found.")
        sys.exit(1)

    splits = image_splitter.split_image(fname=filename, dry_run=False)

    for idx, split in enumerate(splits):
        print(f"{idx+1}. {split}")

    selected_partitions = list()

    while True:
        try:
            partition = input(
                "\nImage splitted, select partition to analyze (A for all partitions): "
            )

            if partition in ["A", "a"]:
                print("All partitions selected")
                selected_partitions = splits[:]
            elif int(partition) in range(1, len(splits) + 1):
                print(f"Selected partition #{int(partition)}")
                selected_partitions.append(splits[int(partition) - 1])
            elif type(partition) not in [int, str] or int(partition) not in range(
                1, len(splits) + 1
            ):
                raise ValueError("Wrong partition selection, try again")
        except ValueError as e:
            print(f"Error: {e}")
            continue
        break
    
    for partition in selected_partitions:
        run_tests(partition)

if __name__ == "__main__":
    main()