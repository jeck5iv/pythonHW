# Matrix Operations

Простая библиотека для работы с матрицами:

## Основные возможности
- Сложение (`+`), умножение (`*`), матричное умножение (`@`)
- Поддержка как чистого Python (Matrix), так и NumPy операций (ExtendedMatrix)
- Кэширование результатов умножения матриц (CachedExtendedMatrix)
- Сохранение/загрузка матриц в файлы

## Использование
```python
from matrix import Matrix, ExtendedMatrix, CachedExtendedMatrix

# Создание матриц
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

# Операции
C = A + B  # Сложение
D = A @ B  # Матричное умножение

# Расширенная матрица с кэшированием
E = CachedExtendedMatrix([[1, 2], [3, 4]])
F = CachedExtendedMatrix([[5, 6], [7, 8]])
G = E @ F  # Результат кэшируется
```

## Требования
- python 3.10+
- numpy (для ExtendedMatrix и CachedExtendedMatrix)
