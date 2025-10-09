

class LimitedStack:
    def __init__(self, max_size=4):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if self.__len__() >= self.max_size:
            raise OverflowError('Stack is full') # raise exception if full
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise IndexError("Stack is empty!")  # raise exception if empty
        return self.items.pop()

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f'Stack "{self.items}"'

stack = LimitedStack()

stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)
print(stack)

try:
    stack.push(5)
    print(stack)
except OverflowError as e:
    print(e)

