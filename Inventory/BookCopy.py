# Resposibility : Hold the State of each physical copy and ability to mutate it's state.
from enums import Book_State
from datetime import date, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Members.Member import Member

class BookCopy:
    def __init__(self, book, barcode: str):
        self.title = book
        self.barcode = barcode
        self.state = Book_State.AVAILABLE
        self.borrower = None
        self.due_date = None
        self.reservation = None
        self.reservation_due = None

    def can_be_borrowed(self) -> bool:
        if self.state == Book_State.AVAILABLE:
            return True
        return False

    def borrow_copy(self, member: "Member", due_date: date) -> None:
        if not self.can_be_borrowed():
            return None
        self.borrower = member
        self.state = Book_State.BORROWED
        self.due_date = due_date
        return None

    def return_copy(self) -> None:
        self.borrower = None
        self.state = Book_State.AVAILABLE
        self.due_date = None
        return None