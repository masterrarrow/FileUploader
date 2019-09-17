from time import sleep
from collections import namedtuple
from multiprocessing import Process, Queue


# Track a progress
Progress = namedtuple('Progress', ['done', 'error', 'total'])


def worker(input_queue, result_queue):
    """
        Worker processes

        :param input_queue: Input data - function and file (Queue)
        :param result_queue: Operation result (Queue)
    """
    for func, file in iter(input_queue.get, None):
        result = func(file)
        result_queue.put(f'{file}, {result}')


def send_file(file):
    """
        Emulate sending file via network

        :param file: File for sending via network
    """
    sleep(2)
    return True


class Uploader(Process):
    def __init__(self, files: list, proc_number: int, result_queue: Queue, *args, **kwargs):
        """
            Send Files via network in parallel processes

            :param files: Files (file name) for sending via network
            :param proc_number: Number of simultaneously running processes
            :param result_queue: Result of the operation (Progress - namedtuple)
        """
        super().__init__(*args, **kwargs)
        self.files = files
        self.proc_number = proc_number
        self.queue = result_queue
        self.task_queue = Queue()
        self.processes = []

        # Submit tasks
        for file in self.files:
            self.task_queue.put([send_file, file])

    def run(self):
        """
            Run parallel processes
        """
        # Queues for results
        result_queue = Queue()

        # Start worker processes
        for i in range(self.proc_number):
            if i < len(self.files):
                self.processes.append(Process(target=worker,
                                              args=(self.task_queue, result_queue)))
                self.processes[-1].daemon = True
                self.processes[-1].start()

        # Get the operation results
        for i in range(len(self.files)):
            file, result = result_queue.get().split(', ')
            done = file if result == 'True' else None
            error = file if result != 'True' else None
            # Track a progress
            total = (100/len(self.files))*(i+1)
            self.queue.put(Progress(f'Done: {done}', f'Errors: {error}', f'Total: {total} %'))

        # Stop child processes
        for i in range(self.proc_number):
            self.task_queue.put(None)

        print('Done successfully!')
