import argparse

import funcsions
import matplotlib.pyplot as plt


def main(file_name):
    """
    Точка входа

    Args:
        file_name: Путь к файлу, из которого будет считываться матрица

    Returns: None

    """

    a = funcsions.read_file_to_sparse_matrix("./Cases/" + file_name)

    print("Исходная матрица:")
    print(a.toarray(), "\n")

    b = funcsions.shift(a)
    print("Циклически сдвинутая матрица:")
    print(b.toarray())

    funcsions.visualize_matrices(a.toarray(), b.toarray())

    plt.savefig(f"./Images/{file_name}.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # Добавляем аргументы командной строки
    parser = argparse.ArgumentParser(
        description="Циклический сдвиг вправо CS матрицы"
    )
    parser.add_argument(
        "path", help="Путь к .txt файлу, из которого будет считываться матрица"
    )

    # Получаем аргументы аргументы
    args = parser.parse_args()

    main(args.path)
