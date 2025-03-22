from concurrent.futures import ProcessPoolExecutor

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter

from statsmodels.graphics.regressionplots import plot_ceres_residuals


def plot_file_cdf(filename_unopt: str, filename_opt: str, bs: int) -> None:
    n_unopt = 0
    n_opt = 0
    counter_unopt = Counter("")
    counter_opt = Counter("")

    with open(filename_unopt, 'rb') as unopt_file, open(filename_opt, 'rb') as opt_file:
        while True:
            chunk_unopt = unopt_file.read(bs)
            if not chunk_unopt:
                break
            n_unopt += len(chunk_unopt)
            print(n_unopt/1024/1024, end='\r')
            counter_unopt += Counter(chunk_unopt)
            del chunk_unopt
        print()
        while True:
            chunk_opt = opt_file.read(bs)
            if not chunk_opt:
                break
            n_opt += len(chunk_opt)
            print(n_opt / 1024 / 1024, end='\r')
            counter_opt += Counter(chunk_opt)
            del chunk_opt

    # Створюємо емпіричну функцію розподілу
    empirical_cdf_unopt = calculate_emp_cdf(counter_unopt, n_unopt)
    empirical_cdf_opt = calculate_emp_cdf(counter_opt, n_opt)

    # Теоретична функція розподілу (рівномірний розподіл)
    theoretical_cdf = np.linspace(1 / 256, 1, 256)

    plt.figure(figsize=(8,6))
    sns.kdeplot(data = theoretical_cdf, cumulative = True, label = "Теоретическое распределение")
    sns.kdeplot(data = empirical_cdf_unopt, cumulative = True, label = filename_unopt.split('/')[-1])
    # sns.kdeplot(data = empirical_cdf_opt, cumulative = True, label = filename_opt.split('/')[-1])
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig(f"/home/gilah/cdf_{filename_unopt.split('/')[-1]}_{filename_opt.split('/')[-1]}.png")


def calculate_emp_cdf(counter: Counter, n):
    empirical_cdf = np.zeros(256)
    cumsum = 0
    for i in range(256):
        cumsum += counter.get(i, 0)
        empirical_cdf[i] = cumsum / n
    return empirical_cdf

with ProcessPoolExecutor(max_workers=8) as executor:
    executor.submit(plot_file_cdf,"/dataset/images/random.img", "/dataset/images/plaintext.txt", bs=1048576)
    # executor.submit(plot_file_cdf,"/dataset/images/wd400.img", "/dataset/images/wd400_opt.img", bs=1048576)
    # executor.submit(plot_file_cdf,"/dataset/images/kagura/kagura_data_dec.img", "/dataset/images/kagura/kagura_data_dec_opt.img", bs=1048576)
    # executor.submit(plot_file_cdf,"/dataset/images/kagura/kagura_data_enc.img", "/dataset/images/kagura/kagura_data_enc_opt.img", bs=1048576)
    # executor.submit(plot_file_cdf,"/dataset/images/miatoll/miatoll_data_fbe.img", "/dataset/images/miatoll/miatoll_data_fbe_opt.img", bs=1048576)
    # executor.submit(plot_file_cdf,"/dataset/images/miatoll/miatoll_data_nonfbe.img", "/dataset/images/miatoll/miatoll_data_nonfbe_opt.img", bs=1048576)
    # executor.submit(plot_file_cdf,"/dataset/images/vince/vince_data.img", "/dataset/images/vince/vince_data_opt.img", bs=1048576)
