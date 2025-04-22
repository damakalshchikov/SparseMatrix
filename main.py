import numpy as np
from funcsions.read_file import read_file_to_sparse_matrix

file_path = "./Cases/test.txt"
A = read_file_to_sparse_matrix(file_path)

matrix = np.array(A.todense())
print(matrix)
