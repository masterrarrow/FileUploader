import unittest
from multiprocessing import Queue
from uploader import Uploader


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.files_1 = [str(i)+'.txt' for i in range(5)]
        self.number_of_processes_1 = 10
        self.q_1 = Queue()

        self.files_2 = [str(i) + '.txt' for i in range(30)]
        self.number_of_processes_2 = 8
        self.q_2 = Queue()

    def test_setup_one(self):
        uploader_1 = Uploader(self.files_1, self.number_of_processes_1, self.q_1)
        uploader_1.start()

        results = [f'Done: {file}' for file in self.files_1]

        for file in self.files_1:
            progress = self.q_1.get()
            self.assertIn(progress.done, results)
            self.assertEqual(progress.error, f'Errors: None')

    def test_setup_two(self):
        uploader_2 = Uploader(self.files_2, self.number_of_processes_2, self.q_2)
        uploader_2.start()

        res = [f'Done: {file}' for file in self.files_2]

        for f in self.files_2:
            progress = self.q_2.get()
            self.assertIn(progress.done, res)
            self.assertEqual(progress.error, f'Errors: None')


if __name__ == '__main__':
    unittest.main()

