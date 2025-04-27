import argparse
import time

import functions
import matplotlib.pyplot as plt
from functions.cyclical_shift_opt import shift_optimized


def main(file_name, mode=1, n=None, m=None, grade=None):
    """
    Точка входа

    Args:
        file_name: Путь к файлу, из которого будет считываться матрица

    Returns: None

    """

    if mode == 2:
        file_name = functions.generate_sparse_matrix_file(n, m, grade, file_name)

    a = functions.read_file_to_sparse_matrix("./Cases/" + file_name)

    # print("Исходная матрица:")
    # print(a.toarray(), "\n")

    start_time = time.time()
    b = shift_optimized(a)
    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.6f} секунд\n")

    # print("Циклически сдвинутая матрица:")
    # print(b.toarray())

    functions.visualize_matrices(a.toarray(), b.toarray())

    plt.savefig(f"./Images/{file_name}.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # Добавляем аргументы командной строки
    parser = argparse.ArgumentParser(
        description="Циклический сдвиг вправо CS матрицы"
    )

    parser.add_argument(
        "path", help="Путь к .txt файлу, из которого будет считываться матрица"
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=int,
        default=1,
        help="Режим работы программы (1 - чтение из файла, 2 - генерация матрицы)",
    )

    parser.add_argument(
        "-n",
        "--n",
        type=int,
        default=None,
        help="Количество строк матрицы (только для режима 2)",
    )

    parser.add_argument(
        "-k",
        "--m",
        type=int,
        default=None,
        help="Количество столбцов матрицы (только для режима 2)",
    )

    parser.add_argument(
        "-g",
        "--grade",
        type=float,
        default=None,
        help="Плотность матрицы (только для режима 2)",
    )
    # Получаем аргументы аргументы
    args = parser.parse_args()

    main(args.path, args.mode, args.n, args.m, args.grade)
