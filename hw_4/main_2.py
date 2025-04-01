import math
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

def worker(args):
    start_idx, end_idx, f, a, step = args
    acc = 0
    for i in range(start_idx, end_idx):
        acc += f(a + i * step) * step
    return acc

def integrate_parallel(f, a, b, n_jobs=1, n_iter=10_000_000, use_threads=True):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs

    tasks = [(i * chunk_size, (i + 1) * chunk_size, f, a, step) for i in range(n_jobs)]
    tasks[-1] = (tasks[-1][0], n_iter, f, a, step)

    executor_cls = ThreadPoolExecutor if use_threads else ProcessPoolExecutor

    with executor_cls(max_workers=n_jobs) as executor:
        results = list(executor.map(worker, tasks))

    return sum(results)

def main():
    a, b = 0, math.pi / 2
    cpu_num = multiprocessing.cpu_count()
    n_jobs_list = list(range(1, cpu_num * 2 + 1))

    results = []

    for n_jobs in n_jobs_list:
        start_time = time.time()
        result_threads = integrate_parallel(math.cos, a, b, n_jobs=n_jobs, use_threads=True)
        time_threads = time.time() - start_time

        start_time = time.time()
        result_processes = integrate_parallel(math.cos, a, b, n_jobs=n_jobs, use_threads=False)
        time_processes = time.time() - start_time

        results.append((n_jobs, time_threads, time_processes))
    
    with open('artifacts/2.txt', 'w') as f:
        f.write(f"CPU cores: {cpu_num}\n")
        f.write("n_jobs | Threads Time | Processes Time\n")
        f.write("--------------------------------------\n")
        for n_jobs, time_threads, time_processes in results:
            f.write(f"{n_jobs:6} | {time_threads:11.5f} | {time_processes:13.5f}\n")

if __name__ == '__main__':
    main()