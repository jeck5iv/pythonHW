from lib.matrix_cache import CachedExtendedMatrix
from lib.utils import save_matrix
import numpy as np

# жёстко заданные матрицы, гарантирующие коллизию
A = CachedExtendedMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
C = CachedExtendedMatrix([[1, 0, 0], [0, 5, 0], [0, 0, 9]])
B = D = CachedExtendedMatrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

print(f"hash(A) = {hash(A)}")
print(f"hash(C) = {hash(C)}")
print(f"A == C? {A.data == C.data}")
print(f"B == D? {B.data == D.data}")

AB = A @ B
CD = C @ D

print(f"A@B:\n{AB.data}")
print(f"C@D:\n{CD.data}")
print(f"A@B == C@D? {AB.data == CD.data}")

assert hash(A) == hash(C) and A.data != C.data
assert B.data == D.data
assert np.any(AB.data != CD.data)

# save_matrix("3_A.txt", A)
# save_matrix("3_B.txt", B)
# save_matrix("3_C.txt", C)
# save_matrix("3_D.txt", D)
# save_matrix("3_AB.txt", AB)
# save_matrix("3_CD.txt", CD)

A.save_to_file("artifacts/3_A.txt")
B.save_to_file("artifacts/3_B.txt") 
C.save_to_file("artifacts/3_C.txt")
D.save_to_file("artifacts/3_D.txt")
AB.save_to_file("artifacts/3_AB.txt")
CD.save_to_file("artifacts/3_CD.txt")

with open("artifacts/3_hash.txt", "w") as f:
    f.write(f"hash(A) = {hash(A)}\n"
            f"hash(C) = {hash(C)}\n"
            f"hash(AB) = {hash(AB)}\n"
            f"hash(CD) = {hash(CD)}")
