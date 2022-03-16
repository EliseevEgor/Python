import time
import threading
import multiprocessing

dictionary_n = [100000, 200000, 300000, 400000, 500000, 500000, 400000, 300000, 200000, 100000]
PATH_EASY_FILE = './artifacts/easy/easy.txt'


def fib(n: int):
    curr = 0
    next = 1
    ind = 0
    while ind < n:
        tmp = next
        next += curr
        curr = tmp
        ind += 1
    return curr


def get_time_sync(fun, args):
    start = time.time()
    fun(args)
    total = time.time() - start
    return total


def get_time_parallel(lst):
    start = time.time()
    for worker in lst:
        worker.start()
    for worker in lst:
        worker.join()
    total = time.time() - start
    return total


def run_sync():
    result = 0
    for n in dictionary_n:
        result += get_time_sync(fib, n)

    return result


def run_with_threads():
    threads = []
    for n in dictionary_n:
        threads.append(threading.Thread(target=fib, args=(n,)))

    return get_time_parallel(threads)


def run_with_processes():
    processes = []
    for n in dictionary_n:
        processes.append(multiprocessing.Process(target=fib, args=(n,)))
    return get_time_parallel(processes)


def do_task():
    with open(PATH_EASY_FILE, 'w') as file:
        file.write(f'Synchronously: {run_sync()}\n')
        file.write(f'Threads: {run_with_threads()}\n')
        file.write(f'Processes: {run_with_processes()}\n')
