from datetime import UTC, datetime, timedelta

from enums import Book_State
from Inventory.BookCopy import BookCopy
from repositories.interfaces import BookCopyRepository


class InMemoryBookCopyRepository(BookCopyRepository):
    def __init__(self) -> None:
        self.book_copies: dict[str, BookCopy] = {}

    def add_copy(self, copy: BookCopy) -> None:
        if not copy:
            return
        self.book_copies[copy.copy_id] = copy

    def eligible_to_borrow(self, member_id: str, isbn: str) -> bool:
        # Check if member has any expired borrows
        count = 0
        today = datetime.now(UTC).date()
        for copy in self.book_copies.values():
            if copy.borrower_member_id == member_id:
                if copy.due_date is not None and copy.due_date < today:
                    return False
                if copy.isbn == isbn:
                    return False
                count += 1
        return count < 3

    def fetch_available_copy(self, isbn: str) -> BookCopy | None:
        for copy in self.book_copies.values():
            if (
                copy.isbn == isbn
                and copy.borrower_member_id is None
                and copy.status == Book_State.AVAILABLE
            ):
                return copy
        return None

    def borrow_copy(self, member_id: str, copy: BookCopy) -> bool:
        # Check if the member is eligibile to borrow a copy.
        today = datetime.now(UTC).date()
        due_date = today + timedelta(days=10)
        copy.borrower_member_id = member_id
        copy.borrowed_date = today
        copy.due_date = due_date
        copy.status = Book_State.BORROWED
        self.book_copies[copy.copy_id] = copy
        return True

    def get_copy(self, barcode: str) -> BookCopy | None:
        return self.book_copies.get(barcode)

    def return_copy(self, copy: BookCopy) -> None:
        returned_copy = self.book_copies.get(copy.copy_id)
        if returned_copy is None:
            return
        returned_copy.status = Book_State.AVAILABLE
        returned_copy.borrower_member_id = None
        returned_copy.due_date = None
        returned_copy.reservation_member_id = None
        returned_copy.reservation_expiry = None
        returned_copy.borrowed_date = None
        self.book_copies[returned_copy.copy_id] = returned_copy
        return

    def reserve_copy_for_waiting_member(self, barcode: str, member_id: str) -> bool:
        copy = self.book_copies.get(barcode)
        if copy is None:
            return False
        today = datetime.now(UTC).date()
        reservation_due = today + timedelta(days=1)
        copy.reservation_member_id = member_id
        copy.reservation_expiry = reservation_due
        copy.borrower_member_id = None
        copy.status = Book_State.RESERVED
        return True

    def remove_from_circulation(self, copy: BookCopy, reason: Book_State) -> None:
        if self.book_copies.get(copy.copy_id) is None:
            return
        copy.status = reason
        copy.borrower_member_id = None
        copy.borrowed_date = None
        copy.due_date = None
        copy.reservation_member_id = None
        copy.reservation_expiry = None
        self.book_copies[copy.copy_id] = copy
        return
