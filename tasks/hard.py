from tasks.easy import Matrix


class HashMixin:
    def __hash__(self):
        hash = 0
        for i in range(self.row):
            for j in range(self.col):
                hash += (i + j + 2) * self.storage[i][j]
        return int(hash)


class HashMatrix(Matrix, HashMixin):
    pass
