

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if not self.is_empty() else None

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def get(self, item):
        if item in self.items:
            self.items.remove(item)
            self.items.append(item)
            return item
        return None

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

stack = Stack()

stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)

stack.get(2)
print(stack.is_empty())
print(stack.items)