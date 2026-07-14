from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Inventory.BookCopy import BookCopy

class Member:
    def __init__(self, member_id: str, name: str, member_type: str):
        self.member_id = member_id
        self.name = name
        self.member_type = member_type
        self.borrowed_books = []
        self.active_reservations = []
        self.waiting_lists = []
        self.restriction_status = False

    def can_borrow(self) -> bool:
        count = 0
        # check for any active borrowed_books
        count += len(self.borrowed_books)
        # check for any witing lists or active registration
        # count += len(self.waiting_lists) + (self.active_reservations != None)
        return count < 3

    def borrow_copy(self, copy: "BookCopy"):
        self.borrowed_books.append(copy)
    
    def return_copy(self, copy: "BookCopy"):
        self.borrowed_books.remove(copy)