import numpy as np
import matplotlib.pyplot as plt


def _visualize_sparse_preview(matrix, preview_size=10):
    """
    Выводит и визуализирует первые preview_size x preview_size элементов
    разреженной матрицы без преобразования всей матрицы в плотный формат.

    Args:
        matrix: Разреженная матрица (scipy.sparse)
        preview_size: Размер предварительного просмотра (число строк и столбцов)

    Returns:
        matplotlib.figure.Figure: Объект фигуры с визуализацией
    """

    n_rows, n_cols = matrix.shape
    preview_rows = min(preview_size, n_rows)
    preview_cols = min(preview_size, n_cols)

    preview_matrix = np.zeros((preview_rows, preview_cols))
    mask = (matrix.row < preview_rows) & (matrix.col < preview_cols)
    preview_rows_indices = matrix.row[mask]
    preview_cols_indices = matrix.col[mask]
    preview_data = matrix.data[mask]

    for i in range(len(preview_rows_indices)):
        row = preview_rows_indices[i]
        col = preview_cols_indices[i]
        preview_matrix[row, col] = preview_data[i]

    # Создаем фигуру для визуализации
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f"Первые {preview_rows}x{preview_cols} элементы матрицы")

    # Создаем таблицу с данными
    table = ax.table(
        cellText=[
            [f"{val:.2f}" if val != 0 else "0" for val in row] for row in preview_matrix
        ],
        cellLoc="center",
        loc="center",
        bbox=[0.1, 0.1, 0.8, 0.8],
    )

    # Стилизуем таблицу
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    # Убираем оси
    ax.axis("off")

    return fig, preview_matrix


def compare_sparse_matrices(
    matrix1, matrix2, preview_size=10, titles=("До:", "После:")
):
    """
    Создает визуализацию сравнения двух разреженных матриц.

    Args:
        matrix1: Первая разреженная матрица
        matrix2: Вторая разреженная матрица
        preview_size: Размер предварительного просмотра
        titles: Кортеж заголовков для каждой матрицы

    Returns:
        matplotlib.figure.Figure: Объект фигуры с визуализацией
    """
    _, preview1 = _visualize_sparse_preview(matrix1, preview_size)
    _, preview2 = _visualize_sparse_preview(matrix2, preview_size)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Первая матрица
    ax1.set_title(titles[0])
    table1 = ax1.table(
        cellText=[
            [f"{val:.2f}" if val != 0 else "0" for val in row] for row in preview1
        ],
        cellLoc="center",
        loc="center",
        bbox=[0.1, 0.1, 0.8, 0.8],
    )

    # Вторая матрица
    ax2.set_title(titles[1])
    table2 = ax2.table(
        cellText=[
            [f"{val:.2f}" if val != 0 else "0" for val in row] for row in preview2
        ],
        cellLoc="center",
        loc="center",
        bbox=[0.1, 0.1, 0.8, 0.8],
    )

    # Стилизуем таблицы
    for table in [table1, table2]:
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

    # Убираем оси
    ax1.axis("off")
    ax2.axis("off")

    plt.tight_layout()

    return fig


def visualize_sparse_matrix_regions(matrix, title, region_size=5):
    """
    Визуализирует 9 ключевых областей разреженной матрицы:

    Каждая область имеет размер region_size x region_size.

    Args:
        matrix: Разреженная матрица (scipy.sparse)
        title: Заголовок для визуализации
        region_size: Размер каждой отображаемой области (по умолчанию 5x5)

    Returns:
        matplotlib.figure.Figure: Объект фигуры с визуализацией
    """
    n_rows, n_cols = matrix.shape
    mid_col = n_cols // 2 - region_size // 2

    regions = [
        ("Верхний левый угол", 0, 0),
        ("Верхняя середина", 0, mid_col),
        ("Верхний правый угол", 0, n_cols - region_size),
        ("Левая середнина", 0, mid_col),
        ("Середина", mid_col, mid_col),
        ("Правая середина", mid_col, 0),
        ("Нижний левый угол", n_rows - region_size, 0),
        ("Нижняя середина", n_rows - region_size, mid_col),
        ("Нижний правый угол", n_rows - region_size, n_cols - region_size),
    ]

    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    axes = axes.flatten()

    # Для каждой области получаем данные и создаем визуализацию
    for idx, (region_name, start_row, start_col) in enumerate(regions):
        region_matrix = np.zeros((region_size, region_size))
        row_mask = (matrix.row >= start_row) & (matrix.row < start_row + region_size)
        col_mask = (matrix.col >= start_col) & (matrix.col < start_col + region_size)
        mask = row_mask & col_mask

        region_rows = matrix.row[mask] - start_row
        region_cols = matrix.col[mask] - start_col
        region_data = matrix.data[mask]

        for i in range(len(region_rows)):
            row = region_rows[i]
            col = region_cols[i]
            region_matrix[row, col] = region_data[i]

        ax = axes[idx]
        ax.set_title(f"{region_name}")

        table = ax.table(
            cellText=[
                [f"{val:.2f}" if val != 0 else "0" for val in row]
                for row in region_matrix
            ],
            cellLoc="center",
            loc="center",
            bbox=[0.05, 0.05, 0.9, 0.9],
        )

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        ax.axis("off")

    plt.tight_layout()
    plt.suptitle(title, fontsize=16)
    plt.subplots_adjust(top=0.9)

    return fig
