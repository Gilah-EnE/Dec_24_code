import time
from collections import Counter
from typing import List, Union, Any

import numpy as np


def calculate_pearson_criterion(filename: str, n: int, byte_counts: Counter) -> tuple[str, int | Any]:
    # Очікувана кількість для рівномірного розподілу
    expected = n / 256

    # Розрахунок критерію Пірсона
    chi_square = 0
    for byte_value in range(256):
        observed = byte_counts.get(byte_value, 0)
        chi_square += (observed - expected) ** 2 / expected

    return filename, chi_square


def interpret_pearson_result(
    chi_square: float, significance_level: float = 0.05
) -> str:
    """
    Інтерпретує результат критерію Пірсона для рівня значущості.

    Args:
        chi_square: Значення критерію Пірсона
        significance_level: Рівень значущості (за замовчуванням 0.05)

    Returns:
        bool: True якщо розподіл можна вважати рівномірним, False в іншому випадку
    """
    # Критичне значення для рівня значущості 0.05 і 255 ступенів свободи
    critical_value = 293.25  # для alpha = 0.05

    if chi_square <= critical_value:
        return "Розподіл можна вважати рівномірним"
    elif chi_square > critical_value:
        return "Розподіл відхиляється від рівномірного"
