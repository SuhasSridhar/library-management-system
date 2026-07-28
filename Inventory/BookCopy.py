# Resposibility : Hold the State of each physical copy and ability to mutate it's state.
from datetime import date, datetime, timedelta, timezone
from typing import TYPE_CHECKING

from enums import Book_State

if TYPE_CHECKING:
    from Members.Member import Member

class BookCopy:
    def __init__(self, book, barcode: str) -> None:
        self.book = book
        self.barcode = barcode
        self.state = Book_State.AVAILABLE
        self.borrower: Member | None = None
        self.due_date: date | None = None
        self.reservation: Member | None = None
        self.reservation_due: date | None = None

    # Method to check if the copy is availble to be borrowed.
    def can_be_borrowed(self) -> bool:
        return self.state == Book_State.AVAILABLE

    # Method to update the state of Book Copy to Borrowed and Store the record of who borrowed.
    def borrow_copy(self, member: "Member", due_date: date) -> None:
        if not self.can_be_borrowed():
            return
        self.borrower = member
        self.state = Book_State.BORROWED
        self.due_date = due_date

    # Method to process the state of a returned Copy.
    def return_copy(self) -> None:
        self.borrower = None
        self.state = Book_State.AVAILABLE
        self.due_date = None
    
    # Method to process the state of a Copy that is to be Reserved for a Waitlist member.
    def reserve_copy(self, member: Member) -> None:
        self.borrower = None
        self.reservation = member
        today = datetime.now(timezone.utc).date()
        reservation_due = today + timedelta(days=1)
        self.reservation_due = reservation_due
        self.state = Book_State.RESERVED

    # Method to check if the copy has expired reservation
    def is_reservation_expired(self) -> bool:
        today = datetime.now(timezone.utc).date()
        return self.state == Book_State.RESERVED and self.reservation_due < today
    
    # Method to Update the State of Expired Reservations
    def cancel_reservation(self) -> None:
        self.reservation = None
        self.reservation_due = None
        self.state = Book_State.AVAILABLE

    def is_valid_retire_state(self, reason: Book_State) -> bool:
        return reason == Book_State.REMOVED or reason == Book_State.LOST or reason == Book_State.DAMAGED
    
    def remove_from_circulation(self, reason: Book_State) -> None:
        self.state = reason
        self.reset_state()

    def is_reserved(self) -> bool:
        return self.reservation is not None

    def is_borrowed(self) -> bool:
        return self.borrower is not None

    def reset_state(self) -> None:
        self.borrower = None
        self.due_date = None
        self.reservation = None
        self.reservation_due = None