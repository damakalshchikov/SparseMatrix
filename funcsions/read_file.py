import numpy as np
from scipy.sparse import coo_matrix


def read_file_to_sparse_matrix(file_path):
    """
    Читает текстовый файл и преобразует его содержимое в разрежённую матрицу.

    Args:
        file_path: Путь к текстовому файлу.

    Returns:
        coo_matrix: Разреженная матрица в формате COO (Coordinate List).

    """
    array = np.loadtxt(file_path, dtype=float)

    rows = array[:, 0].astype(int)  # кол-во строк
    cols = array[:, 1].astype(int)  # кол-во столбцов
    data = array[:, 2]  # значения

    # Определяем размерность матрицы
    n_rows = int(np.max(rows)) + 1
    n_cols = int(np.max(cols)) + 1

    matrix = coo_matrix((data, (rows, cols)), shape=(n_rows, n_cols))

    return matrix
