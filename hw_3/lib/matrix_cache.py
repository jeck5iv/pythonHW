import numpy as np
from lib.matrix_extended import ExtendedMatrix

class HashMixin:
    """Примесь для хэширования матриц через сумму диагонали."""
    def __hash__(self):
        mod = 10**9 + 7
        return sum(self.data[i][i] for i in range(min(len(self.data), len(self.data[0])))) % mod

class CachedMatMulMixin:
    """Примесь для кэширования матричного умножения."""
    _cache = {}

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key in self._cache:
            cached_self, cached_other, result = self._cache[key]
            if np.array_equal(self.data, cached_self.data) and np.array_equal(other.data, cached_other.data):
                return result
        
        result = self.__class__((np.array(self.data) @ np.array(other.data)).tolist())
        self._cache[key] = (self, other, result)
        return result


class CachedExtendedMatrix(ExtendedMatrix, HashMixin, CachedMatMulMixin):
    """Расширенный класс с примесями и хэшированием"""

    def __hash__(self):
        return HashMixin.__hash__(self)

    def __matmul__(self, other):
        return CachedMatMulMixin.__matmul__(self, other)
