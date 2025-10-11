import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Execution time: {time.time() - start:.4f} seconds')
        return result
    return wrapper

@timer
def slow_task():
    for i in range(10):
        i = i +1
        print(i)

slow_task()



