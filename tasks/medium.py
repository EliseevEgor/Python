import numpy as np


class MatrixNPException(Exception):
    pass


class MatrixNP:
    def __init__(self, array):
        super().__init__()
        self._arr = array
        self._row, self._col = array.shape

    @property
    def arr(self):
        return self._arr

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @arr.setter
    def arr(self, value):
        self._arr = value
        self._row, self._col = value.shape

    @row.setter
    def row(self, value):
        self._row = value

    @col.setter
    def col(self, value):
        self._col = value

    def __str__(self):
        return str(self._arr)


class OperationMixin:
    def check_for_add_mul(self, other):
        if isinstance(other, MatrixNP):
            if (self.row, self.col) != (other.row, other.col):
                raise MatrixNPException()
        if (self.row, self.col) != other.shape:
            raise MatrixNPException()

    def check_for_matmul(self, other):
        if isinstance(other, MatrixNP):
            if self.col != other.row:
                raise MatrixNPException()
        if self.col != other.shape[0]:
            raise MatrixNPException()

    def __add__(self, other):
        self.check_for_add_mul(other)
        if isinstance(other, MatrixNP):
            return self.__class__(self.arr + other.arr)
        return self.__class__(self.arr + other)

    def __mul__(self, other):
        self.check_for_add_mul(other)
        if isinstance(other, MatrixNP):
            return self.__class__(self.arr * other.arr)
        return self.__class__(self.arr * other)

    def __matmul__(self, other):
        self.check_for_matmul(other)
        if isinstance(other, MatrixNP):
            return self.__class__(self.arr @ other.arr)
        return self.__class__(self.arr @ other)

    def write_to_file(self, file: str):
        with open(file, 'w') as file:
            file.writelines('\t'.join(str(j) for j in i) + '\n' for i in self.arr)


class OperationsMatrix(MatrixNP, OperationMixin):
    pass
