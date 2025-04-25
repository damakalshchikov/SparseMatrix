from scipy.sparse import coo_matrix


def shift(matrix):
    """
    Функция для циклического сдвига матрицы на 1 позицию вправо.

    Args:
        matrix: Исходная матрица.

    Returns:
        scipy.sparse._coo.coo_matrix: Циклически сдвинутая матрица.

    """

    # Размеры матрицы
    n_rows, n_cols = matrix.shape

    # Вычисляем линейные индексы элементов
    linear_indices = matrix.row * n_cols + matrix.col

    # Сдвиг линейных индексов на 1 позицию вправо
    shifted_linear_indices = (linear_indices + 1) % (n_rows * n_cols)

    # Преобразуем линейные индексы обратно в координаты строк и столбцов
    new_rows = shifted_linear_indices // n_cols
    new_cols = shifted_linear_indices % n_cols

    # Создаем новую разреженную матрицу с обновленными координатами
    shifted_matrix = coo_matrix(
        (matrix.data, (new_rows, new_cols)), shape=matrix.shape
    )

    return shifted_matrix
