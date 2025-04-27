import numpy as np


def generate_sparse_matrix_file(n, m, grade, filename=None, chunk_size=100000):
    """
    Генерирует текстовый файл со структурой разреженной матрицы.
    Оптимизирован для работы с очень большими матрицами.

    Args:
        n (int): Количество строк матрицы
        m (int): Количество столбцов матрицы
        grade (float): Степень заполнения матрицы (от 0 до 1)
        filename (str, optional): Имя создаваемого файла.
                                Если None, используется формат 'nxm.txt'
        chunk_size (int): Количество элементов, обрабатываемых за раз

    Returns:
        str: Путь к созданному файлу
    """
    print(f"Генерация матрицы размером {n}x{m} с плотностью {grade}")

    # Вычисляем количество ненулевых элементов
    total_cells = n * m

    requested_elements = int(total_cells * grade)

    # Ограничиваем максимальное количество элементов для очень больших матриц
    if requested_elements > 10000000:
        non_zero_count = 10000000
    else:
        non_zero_count = requested_elements

    # Определяем имя файла
    if filename is None:
        filename = f"{n}x{m}.txt"

    file_path = f"./Cases/{filename}"

    # Открываем файл для записи
    with open(file_path, "w") as f:
        # Генерируем и записываем данные порциями
        elements_written = 0
        coord_hash = (
            set()
        )  # Используем хэш-таблицу для отслеживания уникальных координат

        while elements_written < non_zero_count:
            # Определяем размер текущей порции
            current_chunk_size = min(chunk_size, non_zero_count - elements_written)

            # Используем больше координат, чем нужно, чтобы учесть дубликаты
            sample_size = min(current_chunk_size * 2, 1000000)

            # Генерируем координаты и значения для текущей порции
            chunk_rows = np.random.randint(0, n, size=sample_size)
            chunk_cols = np.random.randint(0, m, size=sample_size)
            chunk_values = np.round(np.random.uniform(1.0, 100.0, size=sample_size), 1)

            # Записываем уникальные элементы
            for i in range(sample_size):
                if elements_written >= non_zero_count:
                    break

                coord = (chunk_rows[i], chunk_cols[i])
                if coord not in coord_hash:
                    coord_hash.add(coord)
                    f.write(f"{coord[0]} {coord[1]} {chunk_values[i]:.1f}\n")
                    elements_written += 1

            # Освобождаем память
            del chunk_rows, chunk_cols, chunk_values

            # Если мы генерируем почти все элементы полной матрицы,
            # то можем зациклиться из-за повторяющихся координат
            # В этом случае уменьшаем требуемое количество элементов
            if (
                elements_written < non_zero_count
                and len(coord_hash) > 0.9 * total_cells
            ):
                break

    return filename
