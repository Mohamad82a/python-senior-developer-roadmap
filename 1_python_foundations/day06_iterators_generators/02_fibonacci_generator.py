def fibonacci(limit):
    """Generate Fibonacci numbers"""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a+b

print(list(fibonacci(100)))

