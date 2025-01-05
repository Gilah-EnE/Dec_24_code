from collections import Counter
from typing import List, Union

import numpy as np


def calculate_pearson_criterion(bytes_data: Union[bytes, List[int]]) -> float:
    """
    Розраховує значення критерію Пірсона для набору байтів відносно рівномірного розподілу.

    Args:
        bytes_data: Набір байтів у вигляді bytes або список цілих чисел від 0 до 255

    Returns:
        float: Значення критерію Пірсона
    """
    # Перетворюємо вхідні дані в список байтів, якщо потрібно
    if isinstance(bytes_data, bytes):
        bytes_list = list(bytes_data)
    else:
        bytes_list = bytes_data

    # Перевіряємо коректність вхідних даних
    if not all(0 <= b <= 255 for b in bytes_list):
        raise ValueError("Всі значення повинні бути в діапазоні 0-255")

    # Підраховуємо кількість кожного байту
    byte_counts = Counter(bytes_list)

    # Загальна кількість байтів
    n = len(bytes_list)

    # Очікувана кількість для рівномірного розподілу
    expected = n / 256

    # Розрахунок критерію Пірсона
    chi_square = 0
    for byte_value in range(256):
        observed = byte_counts.get(byte_value, 0)
        chi_square += (observed - expected) ** 2 / expected

    return chi_square


def interpret_pearson_result(
    chi_square: float, significance_level: float = 0.05
) -> bool:
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


with open("test.img", "rb") as file:
    test_bytes = file.read()
chi_square = calculate_pearson_criterion(test_bytes)

print("Статистика Пірсона:", chi_square)
print(interpret_pearson_result(chi_square=chi_square))
