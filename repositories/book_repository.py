from Inventory.Book import Book


class BookRepository:
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book):
        if not book:
            return
        self.books[book.isbn] = book

    def get_book(self, isbn: str) -> Book:
        return self.books.get(isbn)

    def search_by_author(self, author: str) -> list[Book]:
        book_list = []
        for book in self.books.values():
            if author.lower() == book.author.lower():
                book_list.append(book)
        return book_list

    def search_by_title(self, title: str) -> list[Book]:
        book_list = []
        for book in self.books.values():
            if title.lower() == book.title.lower():
                book_list.append(book)
        return book_list