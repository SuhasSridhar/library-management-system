# Responsibility : Biblographic data, and manage the inventory of it's physical copies.
from .BookCopy import BookCopy
from datetime import date, timedelta
from Members.Member import Member
from enums import Waitlist_Outcomes
from collections import deque

class Book:
    def __init__ (self, title, author, isbn):
        self.Book = title
        self.author = author
        self.waiting_list = deque()
        self.wait_list_members = set()
        self.copies = {}
        self.isbn = isbn

    def add_copy(self, barcode):
        copy = BookCopy(self, barcode)
        self.copies[barcode] = copy
        return copy
    
    # Method to fetch an available copy for the given title.
    def get_available_copy(self) -> BookCopy:
        for copy in self.copies.values():
            if copy.can_be_borrowed():
                return copy
        return None
    
    # Method to let a member borrow a copy of the title.
    def borrow_copy(self, member: Member) -> BookCopy:
        copy = self.get_available_copy()
        if copy is None:
            return None
        today = date.today()
        due_date = today + timedelta(days=10)
        copy.borrow_copy(member, due_date)
        return copy
    
    # Method to add a member to the waiting list.
    def add_member_to_waitlist(self, member: Member) -> Waitlist_Outcomes:
        if member.member_id in self.wait_list_members:
            return Waitlist_Outcomes.ALREADY_WAITING
        self.waiting_list.append(member)
        self.wait_list_members.add(member.member_id)
        return Waitlist_Outcomes.SUCCESS
    
    # Method to reserve a copy for the member a top of the waiting list as a copy for the title becomes available.
    def reserve_copy(self, copy: BookCopy):
        if not copy.can_be_borrowed():
            return
        if len(self.waiting_list) > 0:
            waiting_member = self.waiting_list.popleft()
            self.wait_list_members.remove(waiting_member.member_id)
            copy.reserve_copy(waiting_member)
            waiting_member.reserve_copy(copy)

    # Method to return a copy and reserve the newly available copy for waiting member atop of the waiting list.
    def return_copy(self, copy: BookCopy):
        copy.return_copy()
        self.reserve_copy(copy)
    
    # Method to process any reservation Expiry and reassign the Reservation if any waiting members are present.
    def expired_validation(self):
        for copy in self.copies.values():
            if copy.is_reservation_expired():
                reserved_member = copy.reservation
                reserved_member.remove_expired_reservation(copy)
                copy.cancel_reservation()
                self.reserve_copy(copy)
    
    # Method to remove a damaged copy
    def remove_damaged_copy(self, copy: BookCopy):
        copy.remove_damaged_copy()