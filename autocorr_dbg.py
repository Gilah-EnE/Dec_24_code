import math
import os
import time
from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from line_profiler_pycharm import profile


def validate_image_file(image_path: str) -> bool:
    path = Path(image_path)
    return path.exists() and path.is_file() and os.access(path, os.R_OK)


@profile
def read_image_block(image_path: str, offset: int, block_size: int) -> Optional[bytes]:
    try:
        if not validate_image_file(image_path):
            raise ValueError(f"Неможливо прочитати файл образу: {image_path}")

        with open(image_path, "rb") as f:
            f.seek(offset)
            data = f.read(block_size)
            if not data:
                raise EOFError("Досягнуто кінця файлу")
            return data
    except (IOError, OSError) as e:
        print(f"Помилка читання файлу: {e}")
        return None

@profile
def calculate_autocorrelation(data: bytes, max_lag: int = 50):
    values = np.frombuffer(data, dtype=np.uint8)
    values = values - np.mean(values)

    autocorr = []
    for lag in range(max_lag):
        if len(values[lag:]) < 2:  # Перевірка на мінімальну довжину для кореляції
            break
        correlation = np.corrcoef(values[lag:], values[: -lag if lag > 0 else None])[0, 1]
        autocorr.append(correlation)

    return autocorr

@profile
def analyze_block(data: bytes, threshold: float = 0.05) -> Tuple[float, bool]:
    if not data:
        return 0.0, False

    autocorr = calculate_autocorrelation(data)
    if not autocorr:
        return 0.0, False

    mean_autocorr = np.mean(np.abs(autocorr[1:]))  # Пропускаємо lag=0
    is_encrypted = mean_autocorr < threshold

    return mean_autocorr, is_encrypted

@profile
def analyze_image_region(image_path: str, start_offset: int, block_size: int, num_blocks: int = 10) -> List[
    Tuple[int, float, bool]]:
    results = []

    for i in range(num_blocks):
        offset = start_offset + (i * block_size)
        data = read_image_block(image_path, offset, block_size)

        if (offset / 1024 / 1024) % 1 == 0:
            print(offset / 1024 / 1024, end='\r')

        if data is None:
            break

        mean_autocorr, is_encrypted = analyze_block(data)
        if not np.isnan(mean_autocorr):
            results.append((offset, mean_autocorr, is_encrypted))

        del data

    return results

@profile
def plot_analysis_scatter(
        results: List[Tuple[int, float, bool]],
        title: str = "Анализ автокорреляции по сдвигам",
        filename: str = "autocorrelation.png",
):
    if not results:
        print("Данные для визуализации отсутствуют")
        return

    # Розділяємо дані на зашифровані та незашифровані
    encrypted_points = [
        (offset, corr) for offset, corr, is_enc in results if is_enc
    ]
    unencrypted_points = [
        (offset, corr) for offset, corr, is_enc in results if not is_enc
    ]

    plt.figure(figsize=(12, 8))

    # Plotting points
    if encrypted_points:
        enc_x, enc_y = zip(*encrypted_points)
        plt.scatter(
            enc_x, enc_y, c="red", label="Вероятно шифрование", alpha=0.6, s=10
        )

    if unencrypted_points:
        unenc_x, unenc_y = zip(*unencrypted_points)
        plt.scatter(
            unenc_x,
            unenc_y,
            c="blue",
            label="Низкая вероятность",
            alpha=0.6,
            s=10,
        )

    plt.title(title)
    plt.xlabel("Сдвиг (байты)")
    plt.ylabel("Средняя автокорреляция по блоку")
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Форматування осі X у шістнадцятковому форматі
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"0x{int(x):08x}"))
    plt.xticks(rotation=45)

    # Додаємо горизонтальну лінію порогового значення
    plt.axhline(
        y=0.05, color="g", linestyle="--", alpha=0.5, label="Порог определения (0.05)"
    )

    plt.tight_layout()
    plt.savefig(filename)

@profile
def plot_autocorrelation(data: bytes, title: str = "График автокорреляции"):
    """
    Візуалізує автокореляційну функцію

    Args:
        data: Вхідні дані
        title: Заголовок графіка
    """
    if not data:
        print("Данные для визуализации отсутствуют")
        return

    autocorr = calculate_autocorrelation(data)
    if not autocorr:
        print("Недостаточно данных")
        return

    plt.figure(figsize=(12, 8))
    plt.plot(autocorr)
    plt.title(title)
    plt.xlabel("Задержка")
    plt.ylabel("Автокорреляция")
    plt.grid(True)
    plt.show()

@profile
def analyze_image_file(image_path: str, bs: int, plot: bool):
    image_size = os.stat(image_path).st_size
    image_blocks = max(1, int(math.floor(image_size / bs)))

    results = analyze_image_region(image_path, start_offset=0, num_blocks=image_blocks, block_size=bs)

    cumsum = np.cumsum([r[1] for r in results])

    plot, ax = plt.subplots()
    ax.plot(cumsum)
    plt.tight_layout()
    plt.show()

    autocorr_stat = list()
    for _, autocorr, _ in results:
        autocorr_stat.append(autocorr)

    if not autocorr_stat:
        raise ValueError("File is empty")

    # Створення XY-графіку результатів
    if plot:
        plot_analysis_scatter(results,
                              f"Распределение средних значений коэф. автокорреляции в файле \"{image_path.split('/')[-1]}\", размер блока {bs} байт",
                              f"/home/gilah/{image_path.split('/')[-1]}.png")

    print(image_path, np.std(autocorr_stat))

start = time.time()
analyze_image_file('/home/gilah/Dataset/images/vince/vince_data.img', 1024*1024, False)
end = time.time()
print(end - start)