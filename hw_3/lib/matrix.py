import random

class Matrix:
    """Класс для работы с матрицами без использования numpy"""
    
    def __init__(self, data):
        """Инициализация матрицы"""
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Все строки матрицы должны быть одинаковой длины")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __add__(self, other):
        """Cложение матриц"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Размерности матриц не совпадают")
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])
    
    def __mul__(self, other):
        """Покомпонентное умножение"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Размерности матриц не совпадают")
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])
    
    def __matmul__(self, other):
        """Матричное умножение"""
        if self.cols != other.rows:
            raise ValueError("Несовместимые размеры для матричного умножения")
        return Matrix([
            [sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
             for j in range(other.cols)]
            for i in range(self.rows)
        ])
