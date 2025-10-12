

class FileWriter:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        if exc_type:
            print(f'Exception occurred: {exc_val}')


with FileWriter('test2.txt') as file:
    file.write('Hello by using context manager')