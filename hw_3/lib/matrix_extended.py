import numpy as np
from lib.matrix import Matrix

class NumPyArithmeticMixin:
    """Примесь для NumPy арифметики"""
    def __add__(self, other):
        return self.__class__((np.array(self.data) + np.array(other.data)).tolist())

    def __sub__(self, other):
        return self.__class__((np.array(self.data) - np.array(other.data)).tolist())

    def __mul__(self, other):
        return self.__class__((np.array(self.data) * np.array(other.data)).tolist())

    def __truediv__(self, other):
        return self.__class__((np.array(self.data) / np.array(other.data)).tolist())

    def __matmul__(self, other):
        return self.__class__((np.array(self.data) @ np.array(other.data)).tolist())

class FileMixin:
    """Примесь для работы с файлами"""
    def save_to_file(self, filename):
        np.savetxt(filename, self.data, fmt="%d")

    @classmethod
    def load_from_file(cls, filename):
        data = np.loadtxt(filename, dtype=int).tolist()
        return cls(data)

class StrMixin:
    """Примесь для красивого вывода"""
    def __str__(self):
        return np.array_str(np.array(self.data))

class PropertyMixin:
    """Примесь для геттеров и сеттеров"""
    
    @property
    def data(self):
        """Геттер для данных матрицы"""
        return self._data

    @data.setter
    def data(self, new_data):
        """Сеттер для данных матрицы"""
        if not all(len(row) == len(new_data[0]) for row in new_data):
            raise ValueError("Все строки должны быть одинаковой длины")
        self._data = new_data

    @property
    def rows(self):
        """Геттер для количества строк"""
        return len(self._data)

    @property
    def cols(self):
        """Геттер для количества столбцов"""
        return len(self._data[0])

    @property
    def shape(self):
        """Размер матрицы (кортеж)"""
        return self.rows, self.cols

    @property
    def size(self):
        """Общее количество элементов в матрице"""
        return self.rows * self.cols


class ExtendedMatrix(Matrix, NumPyArithmeticMixin, FileMixin, StrMixin, PropertyMixin):
    """Расширенный класс с примесями"""
    
    def __init__(self, data):
        self.data = data.tolist() if isinstance(data, np.ndarray) else data

    def __add__(self, other): return NumPyArithmeticMixin.__add__(self, other)
    def __sub__(self, other): return NumPyArithmeticMixin.__sub__(self, other)
    def __mul__(self, other): return NumPyArithmeticMixin.__mul__(self, other)
    def __truediv__(self, other): return NumPyArithmeticMixin.__truediv__(self, other)
    def __matmul__(self, other): return NumPyArithmeticMixin.__matmul__(self, other)
