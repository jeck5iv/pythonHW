from lib.matrix_extended import ExtendedMatrix
from lib.utils import generate_matrix, save_matrix

A = ExtendedMatrix(generate_matrix(seed=0))
B = ExtendedMatrix(generate_matrix(seed=0))

C_add = A + B
C_sub = A - B
C_mul = A * B
C_matmul = A @ B

A.save_to_file("artifacts/2_A.txt")
B.save_to_file("artifacts/2_B.txt")
C_add.save_to_file("artifacts/2_matrix+.txt")
C_mul.save_to_file("artifacts/2_matrix*.txt")
C_matmul.save_to_file("artifacts/2_matrix@.txt")

# запись и загрузка из файла
A.save_to_file("artifacts/2_saved_A.txt")
A_loaded = ExtendedMatrix.load_from_file("artifacts/2_saved_A.txt")

print("Матрица A из файла:")
print(A_loaded)
