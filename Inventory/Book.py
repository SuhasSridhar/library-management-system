# Responsibility : Biblographic data, and manage the inventory of it's physical copies.
from collections import deque
from datetime import datetime, timedelta, timezone

from enums import Book_State, Member_Type, Waitlist_Outcomes
from Members.Member import Member

from .BookCopy import BookCopy


class Book:
    def __init__ (self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.waiting_list: deque[Member] = deque()
        self.wait_list_members: set[str] = set()
        self.copies: dict[str, BookCopy] = {}
        self.archived_books: dict[str, BookCopy] = {}
        self.available_copy = 0
        self.isbn = isbn

    def add_copy(self, barcode: str) -> BookCopy:
        copy = BookCopy(self, barcode)
        self.copies[barcode] = copy
        return copy

    def check_available_copies(self) -> int:
        count = 0
        for copy in self.copies.values():
            if copy.can_be_borrowed():
                count += 1
        return count
    
    # Method to fetch an available copy for the given title.
    def get_available_copy(self) -> BookCopy | None:
        for copy in self.copies.values():
            if copy.can_be_borrowed():
                return copy
        return None
    
    # Method to let a member borrow a copy of the title.
    def borrow_copy(self, member: Member) -> BookCopy | None:
        copy = self.get_available_copy()
        if copy is None:
            return None
        today = datetime.now(timezone.utc).date()
        due_date = today + timedelta(days=10)
        copy.borrow_copy(member, due_date)
        return copy
    
    # Method to add a member to the waiting list.
    def add_member_to_waitlist(self, member: Member) -> Waitlist_Outcomes:
        if member.member_id in self.wait_list_members:
            return Waitlist_Outcomes.ALREADY_WAITING
        if member.member_type == Member_Type.FACULTY:
            self.waiting_list.appendleft(member)
        else :
            self.waiting_list.append(member)
        self.wait_list_members.add(member.member_id)
        return Waitlist_Outcomes.SUCCESS
    
    # Method to reserve a copy for the member a top of the waiting list as a copy for the title becomes available.
    def reserve_copy(self, copy: BookCopy) -> None:
        if not copy.can_be_borrowed():
            return
        if len(self.waiting_list) > 0:
            waiting_member = self.waiting_list.popleft()
            self.wait_list_members.remove(waiting_member.member_id)
            copy.reserve_copy(waiting_member)
            waiting_member.reserve_copy(copy)

    # Method to return a copy and reserve the newly available copy for waiting member atop of the waiting list.
    def return_copy(self, copy: BookCopy) -> None:
        copy.return_copy()
        self.reserve_copy(copy)
    
    # Method to process any reservation Expiry and reassign the Reservation if any waiting members are present.
    def expired_validation(self) -> None:
        for copy in self.copies.values():
            if copy.is_reservation_expired():
                reserved_member = copy.reservation
                if reserved_member is None:
                    return None
                reserved_member.remove_expired_reservation(copy)
                copy.cancel_reservation()
                self.reserve_copy(copy)
    
    # Method to archive retired copy
    def remove_from_circulation(self, copy: BookCopy, reason: Book_State) -> None:
        if not copy.is_valid_retire_state(reason):
            return
        self.update_member_before_removing_copy(copy)
        copy.remove_from_circulation(reason)
        self.archive_uncirculated_books(copy)

    def update_member_before_removing_copy(self, copy: BookCopy) -> None:
        if copy.is_reserved():
            if copy.reservation is None:
                return None
            copy.reservation.remove_expired_reservation(copy)
        if copy.is_borrowed() and copy.borrower is not None:
            copy.borrower.return_copy(copy)

    def archive_uncirculated_books(self, copy: BookCopy) -> None:
        self.archived_books[copy.barcode] = copy
        del self.copies[copy.barcode]