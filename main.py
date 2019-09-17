from multiprocessing import Queue
from uploader import Uploader

if __name__ == "__main__":
    # Initial data
    files_list = [str(i)+'.txt' for i in range(20)]
    number_of_processes = 12
    q = Queue()

    uploader = Uploader(files_list, number_of_processes, q)
    uploader.start()

    for f in files_list:
        progress = q.get()
        print(progress.done, progress.error, progress.total)
