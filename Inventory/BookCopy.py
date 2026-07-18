# Resposibility : Hold the State of each physical copy and ability to mutate it's state.
from enums import Book_State
from datetime import date, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Members.Member import Member

class BookCopy:
    def __init__(self, book, barcode: str):
        self.Book = book
        self.barcode = barcode
        self.state = Book_State.AVAILABLE
        self.borrower = None
        self.due_date = None
        self.reservation = None
        self.reservation_due = None

    # Method to check if the copy is availble to be borrowed.
    def can_be_borrowed(self) -> bool:
        if self.state == Book_State.AVAILABLE:
            return True
        return False

    # Method to update the state of Book Copy to Borrowed and Store the record of who borrowed.
    def borrow_copy(self, member: "Member", due_date: date) -> None:
        if not self.can_be_borrowed():
            return None
        self.borrower = member
        self.state = Book_State.BORROWED
        self.due_date = due_date
        return None

    # Method to process the state of a returned Copy.
    def return_copy(self) -> None:
        self.borrower = None
        self.state = Book_State.AVAILABLE
        self.due_date = None
        return None
    
    # Method to process the state of a Copy that is to be Reserved for a Waitlist member.
    def reserve_copy(self, member: Member):
        self.borrower = None
        self.reservation = member
        today = date.today()
        reservation_due = today + timedelta(days=1)
        self.reservation_due = reservation_due
        self.state = Book_State.RESERVED

    # Method to check if the copy has expired reservation
    def is_reservation_expired(self) -> bool:
        today = date.today()
        if self.state == Book_State.RESERVED and self.reservation_due < today:
            return True
        return False
    
    # Method to Update the State of Expired Reservations
    def cancel_reservation(self):
        self.reservation = None
        self.reservation_due = None
        self.state = Book_State.AVAILABLE

    def is_valid_retire_state(self, reason: Book_State) -> bool:
        if reason == Book_State.REMOVED or reason == Book_State.LOST or reason == Book_State.DAMAGED:
            return True
        return False
    
    def remove_from_circulation(self, reason: Book_State):
        self.state = reason
        self.reset_state()

    def is_reserved(self) -> bool:
        if self.reservation is not None:
            return True
        return False

    def is_borrowed(self) -> bool:
        if self.borrower is not None:
            return True
        return False

    def reset_state(self):
        self.borrower = None
        self.due_date = None
        self.reservation = None
        self.reservation_due = None