
import time

class Time:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f'Elapsed time: {self.end - self.start:.4f}s')

with Time():
    total = sum(i*i for i in range(100000))

