import concurrent
import math
import multiprocessing
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

PATH_TO_LOG_FILE = './artifacts/medium/logs'
PATH_TO_TIMES_FILE = './artifacts/medium/times'


def future_job(f, a, b, n_iter, threads=True):
    with open(PATH_TO_LOG_FILE, 'a') as file:
        if threads:
            name = threading.current_thread().name
        else:
            name = multiprocessing.current_process().name

        file.writelines([name, f' Start time: {time.time()}', '\n'])
        start = time.time()
        acc = 0
        step = (b - a) / n_iter
        for i in range(int(n_iter)):
            acc += f(a + i * step) * step
        end = time.time()
        file.writelines([name, f' Finish time: {end}', '\n'])
        return acc, end - start


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, threads=True):
    ranges = []

    step = (b - a) / n_jobs
    l = a
    r = a + step
    iter = n_iter / n_jobs
    for i in range(n_jobs):
        ranges.append((l, r))
        l = r + 1
        r += step
    if threads:
        pool = ThreadPoolExecutor(n_jobs)
    else:
        pool = ProcessPoolExecutor(n_jobs)
    with pool as pool:
        futures = []
        for rng in ranges:
            futures.append(pool.submit(future_job, f, rng[0], rng[1], iter, threads))
    result = 0
    for future in concurrent.futures.as_completed(futures):
        result += future.result()[1]

    return result


def run(threads=True):
    results = []
    for n in range(1, 17):
        with open(PATH_TO_LOG_FILE, 'a') as file:
            file.write(f'Number of workers = {n}\n')
            file.flush()
            results.append(integrate(math.cos, 0, math.pi / 2, n_jobs=n, threads=threads))

    with open(PATH_TO_TIMES_FILE, 'a') as file:
        for i, r in enumerate(results):
            file.write(f'Number of workers = {i + 1}, Time = {r}\n')


def do_task():
    open(PATH_TO_LOG_FILE, 'w').close()
    open(PATH_TO_TIMES_FILE, 'w').close()

    with open(PATH_TO_LOG_FILE, 'a') as file:
        file.write('THREADS:\n')
    with open(PATH_TO_TIMES_FILE, 'a') as file:
        file.write('THREADS:\n')
    run(threads=True)
    with open(PATH_TO_LOG_FILE, 'a') as file:
        file.write('\n\n')
    with open(PATH_TO_TIMES_FILE, 'a') as file:
        file.write('\n\n')

    with open(PATH_TO_LOG_FILE, 'a') as file:
        file.write('PROCESSES:\n')
    with open(PATH_TO_TIMES_FILE, 'a') as file:
        file.write('PROCESSES:\n')
    run(threads=False)
