import os
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

    # Вычисляем количество ненулевых элементов
    total_elements = n * m
    non_zero_count = min(int(total_elements * grade), 10000000)  # Ограничиваем максимальное количество элементов
    
    # Для очень больших матриц используем прямую генерацию случайных координат
    rows = np.random.randint(0, n, size=non_zero_count)
    cols = np.random.randint(0, m, size=non_zero_count)
    
    # Убираем дубликаты координат (если они есть)
    coordinates = set()
    unique_coords = []
    
    for i in range(non_zero_count):
        coord = (rows[i], cols[i])
        if coord not in coordinates:
            coordinates.add(coord)
            unique_coords.append(coord)
    
    # Преобразуем в numpy массив
    unique_coords = np.array(unique_coords)
    non_zero_count = len(unique_coords)
    
    # Генерируем случайные значения для ненулевых элементов (от 1.0 до 100.0)
    values = np.round(np.random.uniform(1.0, 100.0, size=non_zero_count), 1)
    
    # Создаем результирующий массив с тремя столбцами: строка, столбец, значение
    result = np.column_stack((unique_coords, values))
    
    result = result[np.lexsort((result[:, 1], result[:, 0]))]
    
    # Определяем имя файла
    if filename is None:
        filename = f"{n}x{m}.txt"
    
    # Создаем директорию Cases, если она не существует
    os.makedirs("Cases", exist_ok=True)
    
    # Путь к файлу
    file_path = os.path.join("Cases", filename)
    
    # Записываем порциями, если файл очень большой
    if len(result) > chunk_size:
        with open(file_path, 'w') as f:
            # Записываем по частям
            for i in range(0, len(result), chunk_size):
                end_idx = min(i + chunk_size, len(result))
                chunk = result[i:end_idx]
                np.savetxt(f, chunk, fmt="%d %d %.1f")
    else:
        # Если размер небольшой, записываем все сразу
        np.savetxt(file_path, result, fmt="%d %d %.1f")

    return filename
