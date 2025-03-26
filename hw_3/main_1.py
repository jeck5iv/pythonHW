from lib.matrix import Matrix
from lib.utils import generate_matrix, save_matrix

A = Matrix(generate_matrix(seed=0))
B = Matrix(generate_matrix(seed=0))

C_add = A + B
C_mul = A * B
C_matmul = A @ B

save_matrix("artifacts/1_A.txt", A)
save_matrix("artifacts/1_B.txt", B)
save_matrix("artifacts/1_matrix+.txt", C_add)
save_matrix("artifacts/1_matrix+.txt", C_add)
save_matrix("artifacts/1_matrix*.txt", C_mul)
save_matrix("artifacts/1_matrix@.txt", C_matmul)
