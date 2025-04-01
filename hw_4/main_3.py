import sys
import time
import multiprocessing
import codecs
from queue import Queue

def process_a(input_queue, output_queue, log_queue):
    message_queue = Queue()
    while True:
        while not input_queue.empty():
            message = input_queue.get()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_queue.put(f"[{timestamp}] Process A received: {message}")
            if message == "exit":
                output_queue.put("exit")
                return
            message_queue.put(message.lower())
            log_queue.put(f"[{timestamp}] Process A stored: {message.lower()}")
        
        if not message_queue.empty():
            next_message = message_queue.get()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_queue.put(f"[{timestamp}] Process A sent: {next_message}")
            output_queue.put(next_message)
        
        time.sleep(5)

def process_b(input_queue, result_queue, log_queue):
    while True:
        message = input_queue.get()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_queue.put(f"[{timestamp}] Process B received: {message}")
        if message == "exit":
            result_queue.put("exit")
            break
        encoded_message = codecs.encode(message, "rot_13")
        log_queue.put(f"[{timestamp}] Process B encoded: {encoded_message}")
        print(f"[{timestamp}] Encoded message: {encoded_message}")
        result_queue.put(encoded_message)

def main():
    queue_a = multiprocessing.Queue()
    queue_b = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    log_queue = multiprocessing.Queue()

    proc_a = multiprocessing.Process(target=process_a, args=(queue_a, queue_b, log_queue))
    proc_b = multiprocessing.Process(target=process_b, args=(queue_b, result_queue, log_queue))

    proc_a.start()
    proc_b.start()

    while True:
        user_input = input("Enter message (or 'exit' to quit): ")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_queue.put(f"[{timestamp}] Main process received input: {user_input}")
        queue_a.put(user_input)
        if user_input == "exit":
            break

    proc_a.join()
    proc_b.join()

    with open("artifacts/3.txt", "w") as log_file:
        while not log_queue.empty():
            log_file.write(log_queue.get() + "\n")
        while not result_queue.empty():
            log_file.write(result_queue.get() + "\n")

if __name__ == "__main__":
    main()