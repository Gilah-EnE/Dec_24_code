import os
from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import shapiro
from sklearn import preprocessing


class DiskImageAnalyzer:
    def __init__(self, block_size: int = 512):
        self.block_size = block_size

    def validate_image_file(self, image_path: str) -> bool:
        """
        Перевіряє чи існує файл образу та чи можна його прочитати

        Args:
            image_path: Шлях до файлу образу

        Returns:
            True якщо файл валідний, інакше False
        """
        path = Path(image_path)
        return path.exists() and path.is_file() and os.access(path, os.R_OK)

    def read_image_block(self, image_path: str, offset: int) -> Optional[bytes]:
        """
        Читає блок даних з файлу образу

        Args:
            image_path: Шлях до файлу образу
            offset: Зміщення від початку в байтах

        Returns:
            Прочитані дані або None у випадку помилки
        """
        try:
            if not self.validate_image_file(image_path):
                raise ValueError(f"Неможливо прочитати файл образу: {image_path}")

            with open(image_path, "rb") as f:
                f.seek(offset)
                data = f.read(self.block_size)
                if not data:
                    raise EOFError("Досягнуто кінця файлу")
                return data
        except (IOError, OSError) as e:
            print(f"Помилка читання файлу: {e}")
            return None

    def calculate_autocorrelation(self, data: bytes, max_lag: int = 50) -> List[float]:
        """
        Обчислює автокореляцію для послідовності байтів

        Args:
            data: Вхідні дані
            max_lag: Максимальне зміщення для обчислення автокореляції

        Returns:
            Список коефіцієнтів автокореляції
        """
        values = np.frombuffer(data, dtype=np.uint8)
        values = values - np.mean(values)

        autocorr = []
        for lag in range(max_lag):
            if len(values[lag:]) < 2:  # Перевірка на мінімальну довжину для кореляції
                break
            correlation = np.corrcoef(
                values[lag:], values[: -lag if lag > 0 else None]
            )[0, 1]
            autocorr.append(correlation)

        return autocorr

    def analyze_block(self, data: bytes, threshold: float = 0.1) -> Tuple[float, bool]:
        """
        Аналізує блок даних на предмет шифрування

        Args:
            data: Блок даних для аналізу
            threshold: Поріг для визначення шифрування

        Returns:
            (середня автокореляція, ознака можливого шифрування)
        """
        if not data:
            return 0.0, False

        autocorr = self.calculate_autocorrelation(data)
        if not autocorr:
            return 0.0, False

        mean_autocorr = np.mean(np.abs(autocorr[1:]))  # Пропускаємо lag=0
        is_encrypted = mean_autocorr < threshold

        return mean_autocorr, is_encrypted

    def analyze_image_region(
        self, image_path: str, start_offset: int, num_blocks: int = 10
    ) -> List[Tuple[int, float, bool]]:
        """
        Аналізує послідовність блоків у файлі образу

        Args:
            image_path: Шлях до файлу образу
            start_offset: Початкове зміщення
            num_blocks: Кількість блоків для аналізу

        Returns:
            Список кортежів (зміщення, середня автокореляція, ознака шифрування)
        """
        results = []

        for i in range(num_blocks):
            offset = start_offset + (i * self.block_size)
            data = self.read_image_block(image_path, offset)

            if data is None:
                break

            mean_autocorr, is_encrypted = self.analyze_block(data)
            if not np.isnan(mean_autocorr):
                results.append((offset, mean_autocorr, is_encrypted))

        return results

    def plot_analysis_scatter(
        self,
        results: List[Tuple[int, float, bool]],
        title: str = "Аналіз автокореляції по зсуву",
    ):
        """
        Створює scatter plot результатів аналізу

        Args:
            results: Список результатів у форматі (зсув, автокореляція, ознака_шифрування)
            title: Заголовок графіка
        """
        if not results:
            print("Немає даних для візуалізації")
            return

        # Розділяємо дані на зашифровані та незашифровані
        encrypted_points = [
            (offset, corr) for offset, corr, is_enc in results if is_enc
        ]
        unencrypted_points = [
            (offset, corr) for offset, corr, is_enc in results if not is_enc
        ]

        plt.figure(figsize=(12, 6))

        # Plotting points
        if encrypted_points:
            enc_x, enc_y = zip(*encrypted_points)
            plt.scatter(
                enc_x, enc_y, c="red", label="Можливо зашифровано", alpha=0.6, s=100
            )

        if unencrypted_points:
            unenc_x, unenc_y = zip(*unencrypted_points)
            plt.scatter(
                unenc_x,
                unenc_y,
                c="blue",
                label="Ймовірно незашифровано",
                alpha=0.6,
                s=100,
            )

        plt.title(title)
        plt.xlabel("Зсув (байти)")
        plt.ylabel("Середня автокореляція")
        plt.grid(True, alpha=0.3)
        plt.legend()

        # Форматування осі X у шістнадцятковому форматі
        ax = plt.gca()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"0x{int(x):08x}"))
        plt.xticks(rotation=45)

        # Додаємо горизонтальну лінію порогового значення
        plt.axhline(
            y=0.1, color="g", linestyle="--", alpha=0.5, label="Поріг шифрування (0.1)"
        )

        plt.tight_layout()
        plt.show()

    def plot_autocorrelation(self, data: bytes, title: str = "Графік автокореляції"):
        """
        Візуалізує автокореляційну функцію

        Args:
            data: Вхідні дані
            title: Заголовок графіка
        """
        if not data:
            print("Немає даних для візуалізації")
            return

        autocorr = self.calculate_autocorrelation(data)
        if not autocorr:
            print("Недостатньо даних для побудови графіка автокореляції")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(autocorr)
        plt.title(title)
        plt.xlabel("Lag")
        plt.ylabel("Автокореляція")
        plt.grid(True)
        plt.show()


# Приклад використання:
def analyze_image_file(image_path: str, plot: bool):
    analyzer = DiskImageAnalyzer()

    # Аналіз великого регіону диску
    results = analyzer.analyze_image_region(image_path, start_offset=0, num_blocks=5000)

    autocorr_stat = list()
    for _, autocorr, _ in results:
        autocorr_stat.append(autocorr)

    if autocorr_stat == []:
        raise ValueError("File is empty")

    # Створення XY-графіку результатів
    if plot:
        analyzer.plot_analysis_scatter(results, "Розподіл автокореляції по зсуву")

    return np.mean(autocorr_stat)
