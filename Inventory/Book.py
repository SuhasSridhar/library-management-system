# Responsibility : Biblographic data, and manage the inventory of it's physical copies.
from .BookCopy import BookCopy
from datetime import date, timedelta
from Members.Member import Member

class Book:
    def __init__ (self, title, author, isbn):
        self.title = title
        self.author = author
        self.waiting_list = []
        self.copies = {}
        self.isbn = isbn

    def add_copy(self, barcode):
        copy = BookCopy(self, barcode)
        self.copies[barcode] = copy
        return copy
    
    def get_available_copy(self) -> BookCopy:
        for copy in self.copies.values():
            if copy.can_be_borrowed():
                return copy
        return None
    
    def borrow_copy(self, member: Member) -> BookCopy:
        copy = self.get_available_copy()
        if copy is None:
            return None
        today = date.today()
        due_date = today + timedelta(days=10)
        copy.borrow_copy(member, due_date)
        return copy