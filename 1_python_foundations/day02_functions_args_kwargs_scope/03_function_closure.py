
def outer_func():
    message = 'hello'

    def inner_func():
        print(message)

    inner_func()
outer_func()

