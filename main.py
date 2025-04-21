from funcsions.read_file import read_file_to_sparse_matrix

file_path = "./Cases/test.txt"
A = read_file_to_sparse_matrix(file_path)
print(A)
