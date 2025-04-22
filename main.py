import funcsions

file_path = "./Cases/test.txt"
A = funcsions.read_file_to_sparse_matrix(file_path)

print("Исходная матрица:")
print(A.toarray(), "\n")

B = funcsions.shift(A)
print("Циклически сдвинутая матрица:")
print(B.toarray())
