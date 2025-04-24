import funcsions
import matplotlib.pyplot as plt


def main(path):
    """
    Точка входа

    Args:
        path: Путь к файлу, из которого будет считываться матрица

    Returns: None

    """

    a = funcsions.read_file_to_sparse_matrix(path)

    print("Исходная матрица:")
    print(a.toarray(), "\n")

    b = funcsions.shift(a)
    print("Циклически сдвинутая матрица:")
    print(b.toarray())

    funcsions.visualize_matrices(a.toarray(), b.toarray())

    plt.savefig("./Images/Matrix.png", dpi=300, bbox_inches="tight")


fig = funcsions.visualize_matrices(A.toarray(), B.toarray())

plt.savefig("./Images/Matrix.png", dpi=300, bbox_inches='tight')
