import threading
import time
from multiprocessing import Process, Pipe, Queue
import codecs

PATH_TO_FILE = './artifacts/hard/log'
IS_RUNNING = True


def log(s):
    with open(PATH_TO_FILE, 'a') as file:
        file.write(s)


def fun_a(queue, pipe):
    while True:
        if not queue.empty():
            s = queue.get()
            log(f'Process A: time = {time.time()}, take message from queue = {s}\n')
            ans = s.lower()
            pipe.send(ans)
            log(f'Process A: time = {time.time()}, send message = {ans}\n')
            time.sleep(5)


def fun_b(pipe_main, pipe_a):
    while True:
        s = pipe_a.recv()
        log(f'Process B: time = {time.time()}, get message from A = {s}\n')
        ans = codecs.encode(s, 'rot_13')
        pipe_main.send(ans)
        log(f'Process B: time = {time.time()}, send message to Main = {ans}\n')


def output(main_process_pipe_b=None):
    while IS_RUNNING:
        if main_process_pipe_b.poll():
            ans = main_process_pipe_b.recv()
            log(f'Main process: time = {time.time()}, get message from B = {ans}\n')
            print(ans)


def do_task():
    open(PATH_TO_FILE, 'w').close()
    queue = Queue()
    main_process_pipe_b, b_process_pipe = Pipe()
    a_process_pipe_b, b_process_pipe_a = Pipe()
    a = Process(target=fun_a, name='A', args=(queue, a_process_pipe_b,))
    b = Process(target=fun_b, name='B', args=(b_process_pipe, b_process_pipe_a))
    stdout_thread = threading.Thread(target=output, args=(main_process_pipe_b,))
    a.start()
    b.start()
    stdout_thread.start()

    while True:
        s = input(">>>")
        if s == 'stop':
            break
        log(f'Main process: time = {time.time()}, input = {s}\n')
        queue.put(s)
        log(f'Main process: time = {time.time()}, put message into queue = {s}\n')

    global IS_RUNNING
    IS_RUNNING = False
    a.terminate()
    b.terminate()
    a.join()
    b.join()
    stdout_thread.join()
