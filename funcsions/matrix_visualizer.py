import matplotlib.pyplot as plt


def visualize_matrix(ax, matrix, title):
    """
    Визуализирует матрицу

    Args:
        ax: Оси
        matrix: Матрица, на которой будет строиться визуализация
        title: Заголовок графика

    Returns:
        Таблица matplotlib.table.Table

    """
    # Заголовок графика
    ax.set_title(title)

    # Таблица
    table = ax.table(
        cellText=[[f"{val:.2f}" if val != 0 else "0" for val in row] for row in matrix],
        cellLoc="center",
        loc="center",
        bbox=[0.1, 0.1, 0.8, 0.8]
    )

    # Убираем оси
    ax.axis("off")

    # Стиль таблицы
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    return table


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

    visualize_matrix(ax1, original_matrix, "До:")
    visualize_matrix(ax2, shifted_matrix, "После:")

    plt.tight_layout()

    return fig
