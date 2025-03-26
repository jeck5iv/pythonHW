import random
import numpy as np
from lib.matrix import Matrix

def generate_matrix(seed, size=(10, 10)):
    """Генерация случайной матрицы"""
    np.random.seed(seed)
    return np.random.randint(0, 10, size).tolist()

def save_matrix(filename, matrix):
    """Сохранение матрицы в файл через явный проход по элементам.
    """
    if isinstance(matrix, Matrix):
        data = matrix.data
    elif isinstance(matrix, (list, tuple)):
        data = matrix
    else:
        raise TypeError("Поддерживаются только Matrix или список списков")

    rows = []
    for row in data:
        row_str = ' '.join(str(elem) for elem in row)
        rows.append(row_str)
    matrix_str = '\n'.join(rows)
    with open(filename, 'w') as f:
        f.write(matrix_str)

def load_matrix(filename):
    """Загрузка матрицы из файла"""
    with open(filename, "r") as f:
        data = [[int(num) for num in line.split()] for line in f]
    return Matrix(data)
