from typing import TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from Inventory.BookCopy import BookCopy
    from Inventory.Book import Book

class Member:
    def __init__(self, member_id: str, name: str, member_type: str):
        self.member_id = member_id
        self.name = name
        self.member_type = member_type
        self.borrowed_books = []
        self.active_reservations = []
        self.waiting_lists = []

    def has_overdue_copies(self) -> bool:
        today = date.today()
        for copy in self.borrowed_books:
            if copy.due_date < today:
                return True
        return False

    # Method to check if the member is Eligible to borrow a copy
    def can_borrow(self) -> bool:
        count = 0
        # check for any active borrowed_books that might be overdue.
        if self.has_overdue_copies():
            return False
        count += len(self.borrowed_books)
        return count < 3
    
    # Method to check if the member is Eligible to join the waiting list
    def waitlist_eligibility(self) -> bool:
        if self.has_overdue_copies():
            return False
        return (len(self.waiting_lists) + len(self.active_reservations)) < 2

    # Method to track the borrowed Copies.
    def borrow_copy(self, copy: "BookCopy"):
        self.borrowed_books.append(copy)
    
    # Method to remove the returned copy
    def return_copy(self, copy: "BookCopy"):
        self.borrowed_books.remove(copy)

    # method to update the title in the user is waiting for
    def add_title_to_waitlist(self, title: "Book"):
        self.waiting_lists.append(title)

    # Method to Update the state of the waitlist to reservation
    def reserve_copy(self, copy: "BookCopy"):
        self.active_reservations.append(copy)
        self.waiting_lists.remove(copy.book)

    # Method to update the reservation state of a copy after the Reservation is expired.
    def remove_expired_reservation(self, copy: BookCopy):
        self.active_reservations.remove(copy)