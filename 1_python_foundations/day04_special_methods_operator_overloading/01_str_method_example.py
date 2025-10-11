class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f'{self.title} by {self.author} in {self.pages} pages'

book = Book('Python', 'Mohamad', 750)
print(book)


