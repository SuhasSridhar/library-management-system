from abc import ABC, abstractmethod
from Inventory.BookCopy import BookCopy
from enums import Book_State

class BookCopyRepository(ABC):

    @abstractmethod
    def add_copy(self, book: BookCopy) -> None:
        ...

    @abstractmethod
    def eligible_to_borrow(self, member_id: str, isbn: str) -> bool:
        ...

    @abstractmethod
    def fetch_available_copy(self, isbn: str) -> BookCopy | None:
        ...

    @abstractmethod
    def borrow_copy(self, isbn: str, copy: BookCopy) -> bool:
        ...

    @abstractmethod
    def return_copy(self, copy: BookCopy) -> None:
        ...

    @abstractmethod
    def reserve_copy_for_waiting_member(self, barcode: str, member_id: str) -> bool:
        ...

    @abstractmethod
    def remove_from_circulation(self, copy: BookCopy, reason: Book_State) -> None:
        ...

    @abstractmethod
    def get_copy(self, isbn: str) -> BookCopy | None:
        ...