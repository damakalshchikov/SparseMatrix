import numpy as np


def generate_sparse_matrix_file(n, m, grade, filename=None, chunk_size=1000000):
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
    total_elements = n * m
    requested_elements = int(total_elements * grade)

    # Ограничиваем максимальное количество элементов для очень больших матриц
    if requested_elements > 100000000:
        print("Предупреждение: количество элементов ограничено до 100 миллионов")
        non_zero_count = 100000000
    else:
        non_zero_count = requested_elements

    # Определяем имя файла
    if filename is None:
        filename = f"{n}x{m}.txt"

    # Для очень больших матриц генерируем и записываем данные порциями
    if non_zero_count > chunk_size:
        with open(f"./Cases/{n}x{m}.txt", "w") as f:
            elements_written = 0
            used_coords = set()

            while elements_written < non_zero_count:
                # Определяем размер
                current_chunk_size = min(chunk_size, non_zero_count - elements_written)

                # Генерируем координаты
                chunk_rows = np.random.randint(
                    0, n, size=current_chunk_size * 2
                )
                chunk_cols = np.random.randint(0, m, size=current_chunk_size * 2)
                chunk_values = np.round(
                    np.random.uniform(1.0, 100.0, size=current_chunk_size * 2), 1
                )

                chunk_coords = list(zip(chunk_rows, chunk_cols))
                new_elements = []

                for i, (row, col) in enumerate(chunk_coords):
                    if elements_written >= non_zero_count:
                        break

                    if (row, col) not in used_coords:
                        used_coords.add((row, col))
                        new_elements.append([row, col, chunk_values[i]])
                        elements_written += 1

                if new_elements:
                    chunk_array = np.array(new_elements)
                    np.savetxt(f, chunk_array, fmt="%d %d %.1f")

    else:
        rows = np.random.randint(0, n, size=non_zero_count)
        cols = np.random.randint(0, m, size=non_zero_count)
        values = np.round(np.random.uniform(1.0, 100.0, size=non_zero_count), 1)

        # Убираем дубликаты координат
        unique_coords = list(set(zip(rows, cols)))
        result = np.column_stack((unique_coords, values[: len(unique_coords)]))
        result = result[np.lexsort((result[:, 1], result[:, 0]))]

        np.savetxt(f"./Cases/{n}x{m}.txt", result, fmt="%d %d %.1f")

    return filename
