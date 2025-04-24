import matplotlib.pyplot as plt
from matplotlib import rcParams


def visualize_matrices(original_matrix, shifted_matrix):
    """
    Визуализирует две матрицы в математическом стиле рядом друг с другом.
    
    Parameters:
        original_matrix (numpy.ndarray): Исходная матрица
        shifted_matrix (numpy.ndarray): Сдвинутая матрица
        
    Returns:
def visualize_matrices(original_matrix, shifted_matrix):
    """
    Визуализирует две матрицы рядом друг с другом

    Args:
        original_matrix: Исходная матрица
        shifted_matrix: Сдвинутая матрица

    Returns:
        matplotlib.figure.Figure: Объект фигуры с визуализацией

    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Отключаем оси для обоих подграфиков
    ax1.axis("off")
    ax2.axis("off")
    
    # Функция для форматирования матрицы в LaTeX
    def format_matrix_latex(matrix, name):
        matrix_str = r"$" + name + r"_{" + f"{m}{n}" + r"} = \begin{pmatrix}"
        
        for i in range(m):
            row_str = " & ".join(
                [f"{val:.2f}" if val != 0 else "0" for val in matrix[i, :]]
            )
            matrix_str += row_str
            if i < m - 1:
                matrix_str += r" \\ "
        
        matrix_str += r"\end{pmatrix}$"
        return matrix_str
    
    # Отображаем исходную матрицу
    original_latex = format_matrix_latex(original_matrix, "A")
    ax1.text(0.5, 0.5, original_latex, size=14, ha="center", va="center")
    ax1.set_title("Исходная матрица")
    
    # Отображаем сдвинутую матрицу
    shifted_latex = format_matrix_latex(shifted_matrix, "B")
    ax2.text(0.5, 0.5, shifted_latex, size=14, ha="center", va="center")
    ax2.set_title("Циклически сдвинутая матрица")
    
    # Настраиваем поля

    visualize_matrix(ax1, original_matrix, "До:")
    visualize_matrix(ax2, shifted_matrix, "После:")

    plt.tight_layout()

    return fig
