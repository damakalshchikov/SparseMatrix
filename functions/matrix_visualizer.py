import numpy as np
import matplotlib.pyplot as plt


def visualize_sparse_preview(matrix, preview_size=10):
    """
    Выводит и визуализирует первые preview_size x preview_size элементов
    разреженной матрицы без преобразования всей матрицы в плотный формат.

    Args:
        matrix: Разреженная матрица (scipy.sparse)
        preview_size: Размер предварительного просмотра (число строк и столбцов)

    Returns:
        matplotlib.figure.Figure: Объект фигуры с визуализацией
    """

    # Ограничиваем размер предварительного просмотра фактическим размером матрицы
    n_rows, n_cols = matrix.shape
    preview_rows = min(preview_size, n_rows)
    preview_cols = min(preview_size, n_cols)

    # Создаем пустую матрицу для предварительного просмотра
    preview_matrix = np.zeros((preview_rows, preview_cols))

    # Находим элементы внутри области предварительного просмотра
    mask = (matrix.row < preview_rows) & (matrix.col < preview_cols)
    preview_rows_indices = matrix.row[mask]
    preview_cols_indices = matrix.col[mask]
    preview_data = matrix.data[mask]

    # Заполняем матрицу предварительного просмотра
    for i in range(len(preview_rows_indices)):
        row = preview_rows_indices[i]
        col = preview_cols_indices[i]
        preview_matrix[row, col] = preview_data[i]

    # Создаем фигуру для визуализации
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f"Первые {preview_rows}x{preview_cols} элементы матрицы")

    # Создаем таблицу с данными
    table = ax.table(
        cellText=[[f"{val:.2f}" if val != 0 else "0" for val in row] for row in preview_matrix],
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


def compare_sparse_matrices(matrix1, matrix2, preview_size=10, titles=("До:", "После:")):
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
    # Получаем превью для обеих матриц
    _, preview1 = visualize_sparse_preview(matrix1, preview_size)
    _, preview2 = visualize_sparse_preview(matrix2, preview_size)

    # Создаем фигуру для сравнения
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Первая матрица
    ax1.set_title(titles[0])
    table1 = ax1.table(
        cellText=[[f"{val:.2f}" if val != 0 else "0" for val in row] for row in preview1],
        cellLoc="center",
        loc="center",
        bbox=[0.1, 0.1, 0.8, 0.8],
    )

    # Вторая матрица
    ax2.set_title(titles[1])
    table2 = ax2.table(
        cellText=[[f"{val:.2f}" if val != 0 else "0" for val in row] for row in preview2],
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
