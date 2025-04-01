import time
import threading
import multiprocessing

def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def run_with_threads(n):
    threads = []
    results = []
    for _ in range(10):
        thread = threading.Thread(target=lambda: results.append(fibonacci(n)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return results

def run_with_processes(n):
    processes = []
    results = []
    for _ in range(10):
        process = multiprocessing.Process(target=lambda: results.append(fibonacci(n)))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    return results

def run_sync(n):
    results = []
    for _ in range(10):
        results.append(fibonacci(n))
    return results

def compare_execution_times(n):
    with open('artifacts/1.txt', 'w') as f:
        for method, func in [("Sync", run_sync), ("Threads", run_with_threads), ("Processes", run_with_processes)]:
            start_time = time.time()
            func(n)
            end_time = time.time()
            elapsed_time = end_time - start_time
            f.write(f"{method} execution time: {elapsed_time:.5f} seconds\n")

if __name__ == "__main__":
    compare_execution_times(300000)
