from collections import Counter
from typing import Tuple, Union
import time
import numpy as np


def calculate_kolmogorov_smirnov(
    filename: str
) -> Tuple[float, dict]:
    n = 0
    counter = Counter("")

    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(512*1024*1024)
            if not chunk:
                break
            n += len(chunk)
            print(n/1024/1024)
            counter += Counter(chunk)
            del chunk

    # Створюємо емпіричну функцію розподілу
    empirical_cdf = np.zeros(256)
    cumsum = 0
    for i in range(256):
        cumsum += counter.get(i, 0)
        empirical_cdf[i] = cumsum / n

    # Теоретична функція розподілу (рівномірний розподіл)
    theoretical_cdf = np.linspace(1 / 256, 1, 256)

    # Розрахунок статистики Колмогорова-Смірнова
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

    return ks_statistic, info


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
    
def calculate_ks_file(partition_path: str):
    ks_statistic, info = calculate_kolmogorov_smirnov(partition_path)

    if ks_statistic <= info['critical_value_005'] or ks_statistic <= info['critical_value_001']:
        return False
    else:
        return True
'''
# test_bytes = bytes([1, 2, 3, 4, 5] * 1000)  # тестові дані

with open("test.img", "rb") as file:
    test_bytes = file.read()
ks_statistic, info = calculate_kolmogorov_smirnov(test_bytes)

print(f"Статистика Колмогорова-Смірнова: {ks_statistic}")
print(f"Критичне значення (α = 0.01): {info['critical_value_001']}")
print(f"Критичне значення (α = 0.05): {info['critical_value_005']}")
print("\nІнтерпретація:")
print(interpret_ks_result(ks_statistic, info["sample_size"]))
'''

start = time.time()
print(calculate_kolmogorov_smirnov("ext4_fs.bin"))
end = time.time()
print(end - start)