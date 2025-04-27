import argparse
import time

import matplotlib.pyplot as plt

import functions


def main(file_name, mode=1, n=None, m=None, grade=None):
    """
    Точка входа

    Args:
        file_name: Путь к файлу, из которого будет считываться матрица
        mode: Режим работы (1 - чтение из файла, 2 - генерация матрицы)
        n: Количество строк (для режима 2)
        m: Количество столбцов (для режима 2)
        grade: Плотность матрицы (для режима 2)

    Returns: None
    """

    if mode == 2:
        file_name = functions.generate_sparse_matrix_file(n, m, grade, file_name)

    a = functions.read_file_to_sparse_matrix("./Cases/" + file_name)
    matrix_size = max(a.shape[0], a.shape[1])

    print(f"Размер матрицы: {a.shape[0]}x{a.shape[1]}")
    print(f"Количество ненулевых элементов: {a.nnz}")

    start_time = time.time()

    # Выбор метода на основе размерности
    if matrix_size > 9999:
        print("Используется оптимизированный метод")
        b = functions.shift_for_huge_matrices(a)
    else:
        print("Используется стандартный метод")
        b = functions.shift_optimized(a)

    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.6f} секунд\n")

    # Визуализация только для небольших матриц
    if matrix_size <= 50:
        functions.visualize_matrices(a.toarray(), b.toarray())
        plt.savefig(
            f"./Images/{file_name.replace('.txt', '')}.png",
            dpi=300,
            bbox_inches="tight",
        )
    else:
        print("Визуализация пропущена из-за большого размера матрицы")
        # Вывод первых нескольких элементов для проверки сдвига
        preview_size = min(10, matrix_size)
        print(f"\nПервые {preview_size}x{preview_size} элементы исходной матрицы:")
        print(a.toarray()[:preview_size, :preview_size])
        print(f"\nПервые {preview_size}x{preview_size} элементы после сдвига:")
        print(b.toarray()[:preview_size, :preview_size])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Циклический сдвиг вправо матрицы")
    parser.add_argument("path", help="Путь к .txt файлу с матрицей")
    parser.add_argument("-m", "--mode", type=int, default=1, help="Режим: 1-чтение, 2-генерация")
    parser.add_argument("-n", type=int, help="Количество строк (режим 2)")
    parser.add_argument("-k", type=int, help="Количество столбцов (режим 2)")
    parser.add_argument("-g", "--grade", type=float, help="Плотность матрицы (режим 2)")

    args = parser.parse_args()
    main(args.path, args.mode, args.n, args.k, args.grade)
