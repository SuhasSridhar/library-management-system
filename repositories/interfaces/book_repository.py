from abc import ABC, abstractmethod
from Inventory.Book import Book

class BookRepository(ABC):

    @abstractmethod
    def add_book(self, book: Book) -> None:
        ...

    @abstractmethod
    def get_book(self, isbn: str) -> Book | None:
        ...

    @abstractmethod
    def search_by_author(self, author: str) -> list[Book]:
        ...

    @abstractmethod
    def search_by_title(self, title: str) -> list[Book]:
        ...