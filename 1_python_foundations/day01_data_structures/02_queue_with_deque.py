from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft() #pops(remove) item from the left
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)

queue = Queue()

queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
queue.enqueue(4)

queue.dequeue()

print(queue.queue)