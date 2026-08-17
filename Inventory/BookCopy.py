# Resposibility : Hold the State of each physical copy and ability to mutate it's state.
from datetime import date

from enums import Book_State


class BookCopy:
    def __init__(self, isbn: str, barcode: str, status: Book_State) -> None:
        self.isbn = isbn
        self.copy_id = barcode
        self.status = status
        self.borrower_member_id: str | None = None
        self.borrowed_date: date | None = None
        self.due_date: date | None = None
        self.reservation_member_id: str | None = None
        self.reservation_expiry: date | None = None