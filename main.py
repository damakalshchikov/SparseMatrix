import funcsions
import matplotlib.pyplot as plt


file_path = "./Cases/test.txt"
A = funcsions.read_file_to_sparse_matrix(file_path)

print("Исходная матрица:")
print(A.toarray(), "\n")

B = funcsions.shift(A)
print("Циклически сдвинутая матрица:")
print(B.toarray())

fig = funcsions.visualize_matrices(A.toarray(), B.toarray())

plt.savefig("matrix_visualization.png", dpi=300, bbox_inches='tight')

plt.show()
