# Responsibility : Biblographic data, and manage the inventory of it's physical copies.
class Book:
    def __init__ (self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn