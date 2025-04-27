from scipy.sparse import coo_matrix


def shift_coo(matrix):
    """
    Функция для циклического сдвига разреженной матрицы на 1 позицию вправо,

    Args:
        matrix: Исходная разреженная матрица

    Returns:
        scipy.sparse.coo_matrix: Циклически сдвинутая матрица
    """
    # Преобразуем в COO, если матрица в другом формате
    if not isinstance(matrix, coo_matrix):
        matrix = matrix.tocoo()

    # Получаем размеры матрицы и данные
    n_rows, n_cols = matrix.shape
    rows = matrix.row.copy()
    cols = matrix.col.copy()
    data = matrix.data.copy()

    # Индексы элементов, которые останутся в той же строке
    same_row_mask = cols < n_cols - 1
    # Индексы элементов, которые перейдут в следующую строку
    next_row_mask = ~same_row_mask

    # Обработка элементов, которые останутся в той же строке (просто увеличиваем столбец)
    cols[same_row_mask] += 1

    # Обработка элементов, которые перейдут на следующую строку
    cols[next_row_mask] = 0  # Переход в начало строки

    # Увеличиваем индекс строки для элементов, переходящих на следующую
    rows[next_row_mask] += 1

    # Обработка элементов из последней строки, которые переходят в начало
    last_row_mask = rows >= n_rows
    rows[last_row_mask] = 0

    # Создаем новую разреженную матрицу
    shifted_matrix = coo_matrix((data, (rows, cols)), shape=matrix.shape)

    return shifted_matrix
