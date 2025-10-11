def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('Before function ' + '*' * 10)
        func(*args, **kwargs)
        print('After function ' + '*' * 10)
    return wrapper

@my_decorator
def say_hello(name):
    print(f'Hello {name}')

say_hello('Mohamad')