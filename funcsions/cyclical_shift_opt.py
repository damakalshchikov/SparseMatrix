from scipy.sparse import coo_matrix, csr_matrix, lil_matrix
import numpy as np
import gc


def shift_optimized(matrix, chunk_size=10000):
    """
    Оптимизированная функция для циклического сдвига разреженной матрицы на 1 позицию вправо.
    Работает эффективно с матрицами очень больших размеров.

    Args:
        matrix: Исходная разреженная матрица (coo_matrix)
        chunk_size: Размер обрабатываемых за один раз данных

    Returns:
        scipy.sparse._coo.coo_matrix: Циклически сдвинутая матрица
    """
    # Получаем размеры матрицы
    n_rows, n_cols = matrix.shape
    print(f"Размер матрицы: {n_rows} x {n_cols}")
    total_elements = matrix.nnz  # Количество ненулевых элементов
    
    # Для более эффективной работы с большими матрицами преобразуем в CSR
    if not isinstance(matrix, coo_matrix):
        matrix = matrix.tocoo()
    
    # Обработка по частям для очень больших матриц
    if n_rows > chunk_size:
        # Инициализируем списки для новых координат и данных
        new_rows = []
        new_cols = []
        data_chunks = []
        
        # Обрабатываем данные порциями
        for i in range(0, total_elements, chunk_size):
            end_idx = min(i + chunk_size, total_elements)
            
            # Выделяем часть данных
            rows_chunk = matrix.row[i:end_idx]
            cols_chunk = matrix.col[i:end_idx]
            data_chunk = matrix.data[i:end_idx]
            
            # Вычисляем линейные индексы для текущей порции
            linear_indices = rows_chunk * n_cols + cols_chunk
            
            # Сдвигаем линейные индексы
            shifted_linear_indices = (linear_indices + 1) % (n_rows * n_cols)
            
            # Преобразуем обратно в координаты
            rows_shifted = shifted_linear_indices // n_cols
            cols_shifted = shifted_linear_indices % n_cols
            
            # Добавляем в общие списки
            new_rows.append(rows_shifted)
            new_cols.append(cols_shifted)
            data_chunks.append(data_chunk)
            
            # Явно освобождаем память для временных массивов
            del rows_chunk, cols_chunk, linear_indices, shifted_linear_indices
            gc.collect()
        
        # Объединяем все обработанные порции
        new_rows = np.concatenate(new_rows)
        new_cols = np.concatenate(new_cols)
        new_data = np.concatenate(data_chunks)
        
    else:
        # Для матриц небольшого размера используем стандартный подход
        linear_indices = matrix.row * n_cols + matrix.col
        shifted_linear_indices = (linear_indices + 1) % (n_rows * n_cols)
        
        new_rows = shifted_linear_indices // n_cols
        new_cols = shifted_linear_indices % n_cols
        new_data = matrix.data
    
    # Создаем новую разреженную матрицу
    shifted_matrix = coo_matrix(
        (new_data, (new_rows, new_cols)), shape=matrix.shape
    )
    
    return shifted_matrix


def shift_for_huge_matrices(matrix, chunk_size=1000000):
    """
    Алгоритм для эффективного сдвига очень больших матриц, 
    использующий комбинацию различных форматов хранения.

    Args:
        matrix: Исходная разреженная матрица
        chunk_size: Размер обрабатываемых за один раз данных

    Returns:
        scipy.sparse.coo_matrix: Циклически сдвинутая матрица
    """
    n_rows, n_cols = matrix.shape
    total_size = n_rows * n_cols
    
    # Для сверхбольших матриц используем LIL формат для построения результата
    if matrix.nnz > 10000000:
        # Преобразуем входную матрицу в COO для итерации по элементам
        if not isinstance(matrix, coo_matrix):
            matrix = matrix.tocoo()
        
        # Создаем пустую матрицу для результата
        result = lil_matrix((n_rows, n_cols))
        
        # Обрабатываем порциями
        for chunk_start in range(0, matrix.nnz, chunk_size):
            chunk_end = min(chunk_start + chunk_size, matrix.nnz)
            
            # Получаем текущую порцию данных
            rows = matrix.row[chunk_start:chunk_end]
            cols = matrix.col[chunk_start:chunk_end]
            data = matrix.data[chunk_start:chunk_end]
            
            # Для каждого элемента вычисляем новую позицию после сдвига
            for i in range(len(rows)):
                # Вычисляем линейный индекс и его сдвиг
                linear_idx = rows[i] * n_cols + cols[i]
                new_linear_idx = (linear_idx + 1) % total_size
                
                # Преобразуем обратно в координаты
                new_row = new_linear_idx // n_cols
                new_col = new_linear_idx % n_cols
                
                # Заполняем результирующую матрицу
                result[new_row, new_col] = data[i]
            
            # Очистка памяти после обработки порции
            del rows, cols, data
            gc.collect()
        
        # Преобразуем результат в COO формат перед возвратом
        return result.tocoo()
    else:
        # Для матриц меньшего размера используем оптимизированную функцию
        return shift_optimized(matrix, chunk_size)
