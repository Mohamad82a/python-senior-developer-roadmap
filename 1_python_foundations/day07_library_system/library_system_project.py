
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        status = 'Borrowed' if self.is_borrowed else 'Available'
        return f"{self.title} by {self.author} - {status} - {self.is_borrowed}"

class Library:
    def __init__(self):
        self.books = []

    def get_book_title(self):
        for book in self.books:
            return book.title

    def add_book(self, title, author):
        self.books.append(Book(title, author))

    def borrow_book(self, title):
        if title.lower() in self.get_book_title().lower():
            for book in self.books:
                if book.title.lower()  == title.lower() and not book.is_borrowed:
                    book.is_borrowed = True
                    print(f'You have borrowed {book.title} by author: {book.author}')
                    return
            print('Book is borrowed')
        else:
            print('Book not found to borrow!')

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.is_borrowed:
                book.is_borrowed = False
                print(f'You have returned {book.title} by author: {book.author}')
                return
        print('Book not found to return!')

    def book_list(self):
        for book in self.books:
            print(book)



library = Library()
library.add_book('Python', 'Mohamad Abbasi')
library.add_book('Django', 'Mehrad Abbasi')
library.add_book('Love', 'Mahsa Khayat')

library.book_list()

library.borrow_book('python')
library.borrow_book('Python')
library.return_book('Python')
library.borrow_book('Python')





