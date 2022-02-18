import numpy as np

from tasks.easy import Matrix
from tasks.hard import HashMatrix
from tasks.medium import OperationsMatrix

FILE_PATH_EASY = 'artifacts/easy/'
FILE_PATH_MEDIUM = 'artifacts/medium/'
FILE_PATH_HARD = 'artifacts/hard/'
PATH_A = 'A.txt'
PATH_B = 'B.txt'
PATH_C = 'C.txt'
PATH_D = 'D.txt'
PATH_AB = 'AB.txt'
PATH_CD = 'CD.txt'
PATH_HASH = 'hash.txt'
PATH_ADD = 'matrix+.txt'
PATH_MUL = 'matrix*.txt'
PATH_MAT_MUL = 'matrix@.txt'


def write_to_file(file: str, m: Matrix):
    with open(file, 'w') as file:
        file.writelines('\t'.join(str(j) for j in i) + '\n' for i in m.storage)


def task1():
    np_a = np.random.randint(0, 10, (10, 10))
    np_b = np.random.randint(0, 10, (10, 10))

    A = Matrix(np_a)
    B = Matrix(np_b)

    write_to_file(FILE_PATH_EASY + PATH_ADD, A + B)
    write_to_file(FILE_PATH_EASY + PATH_MUL, A * B)
    write_to_file(FILE_PATH_EASY + PATH_MAT_MUL, A @ B)


def task2():
    np_a = np.random.randint(0, 10, (10, 10))

    A = OperationsMatrix(np_a)
    B = np.random.randint(0, 10, (10, 10))

    (A + B).write_to_file(FILE_PATH_MEDIUM + PATH_ADD)
    (A * B).write_to_file(FILE_PATH_MEDIUM + PATH_MUL)
    (A @ B).write_to_file(FILE_PATH_MEDIUM + PATH_MAT_MUL)


def task3():
    with open(FILE_PATH_HARD + PATH_A, 'r') as f:
        lst_A = [[int(num) for num in line.split(' ')] for line in f]
    with open(FILE_PATH_HARD + PATH_B, 'r') as f:
        lst_B = [[int(num) for num in line.split(' ')] for line in f]
    with open(FILE_PATH_HARD + PATH_C, 'r') as f:
        lst_C = [[int(num) for num in line.split(' ')] for line in f]
    with open(FILE_PATH_HARD + PATH_D, 'r') as f:
        lst_D = [[int(num) for num in line.split(' ')] for line in f]

    A = HashMatrix(np.array(lst_A))
    B = HashMatrix(np.array(lst_B))
    C = HashMatrix(np.array(lst_C))
    D = HashMatrix(np.array(lst_D))

    A_B = A @ B
    C_D = C @ D
    write_to_file(FILE_PATH_HARD + PATH_AB, A_B)
    write_to_file(FILE_PATH_HARD + PATH_CD, C_D)

    with open(FILE_PATH_HARD + PATH_HASH, 'w') as file:
        file.write(str(hash(A_B)))
        file.write('\n')
        file.write(str(hash(C_D)))


if __name__ == '__main__':
    task1()
    task2()
    task3()
