import time
from collections import Counter
from typing import Tuple
import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns


def calculate_kolmogorov_smirnov(filename: str, n: int, counter: Counter, plot: bool) -> Tuple[float, dict]:
    # Створюємо емпіричну функцію розподілу
    empirical_cdf = np.zeros(256)
    cumsum = 0
    for i in range(256):
        cumsum += counter.get(i, 0)
        empirical_cdf[i] = cumsum / n

    # Теоретична функція розподілу (рівномірний розподіл)
    theoretical_cdf = np.linspace(1 / 256, 1, 256)

    # Розрахунок статистики Колмогорова-Смірнова
    # info = scipy.stats.kstest(empirical_cdf, theoretical_cdf)
    differences = np.abs(empirical_cdf - theoretical_cdf)
    ks_statistic = np.max(differences)
    max_diff_position = np.argmax(differences)

    # Додаткова інформація
    info = {
        "max_difference": ks_statistic,
        "max_difference_position": max_diff_position,
        "max_difference_value": max_diff_position,
        "sample_size": n,
        "critical_value_001": 1.63 / np.sqrt(n),  # Критичне значення для α = 0.01
        "critical_value_005": 1.36 / np.sqrt(n),  # Критичне значення для α = 0.05
    }
    if plot:
        plt.figure(figsize=(12, 8))
        plt.title(f"Распределение байтов в файле {filename.split('/')[-1]}")
        plt.xlabel("Байт")
        plt.ylabel("Количество вхождений")
        plt.grid(True, alpha=0.3)
        plt.bar(counter.keys(), counter.values())
        plt.tight_layout()
        plt.savefig(f"/home/gilah/distrib_{filename.split('/')[-1]}.png")

    return filename, ks_statistic, info['max_difference_position'], info['sample_size'], info['critical_value_001'], info['critical_value_005']


def interpret_ks_result(ks_statistic: float, sample_size: int) -> str:
    """
    Інтерпретує результат тесту Колмогорова-Смірнова.

    Args:
        ks_statistic: Значення статистики Колмогорова-Смірнова
        sample_size: Розмір вибірки

    Returns:
        str: Текстова інтерпретація результату
    """
    critical_001 = 1.63 / np.sqrt(sample_size)
    critical_005 = 1.36 / np.sqrt(sample_size)

    if ks_statistic <= critical_005:
        return "Розподіл можна вважати рівномірним (p > 0.05)"
    elif ks_statistic <= critical_001:
        return "Є незначні відхилення від рівномірного розподілу (0.01 < p ≤ 0.05)"
    else:
        return "Значні відхилення від рівномірного розподілу (p ≤ 0.01)"
