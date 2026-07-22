# Resposibility:
# Represents a single library branch.
# Owns the catalog of books and the registered members.
# Coordinates high-level workflows such as checkout and return.

from Members.Member import Member
from enums import Book_State
from Inventory.Book import Book
from Inventory.BookCopy import BookCopy
from enums import Waitlist_Outcomes

class Library:
    def __init__(self):
        self.members = {}
        self.books = {}

    def add_member(self, member_id: str, name: str, member_type: str) -> str:
        # Add students
        member = Member(
            member_id,
            name,
            member_type
        )
        self.members[member_id] = member
        return member
    
    def add_book(self, title: str, author: str, isbn: str, copies: list[str]) -> Book:
        # Add a title and a few copies for the same
        book = Book(
            title,
            author,
            isbn
        )

        self.books[isbn] = book

        for copy in copies:
            book.add_copy(copy)

        return book
    
    def find_member(self, member_id: str) -> Member:
        if not member_id:
            return None
        return self.members.get(member_id)
    
    def find_book(self, isbn: str) -> Book:
        if not isbn:
            return None
        return self.books.get(isbn)

    def search_by_title(self, title: str) -> list[Book]:
        book_list = list()
        if not title:
            return book_list
        for book in self.books.values():
            if title.lower() == book.title.lower():
                book_list.append(book)
        return book_list

    def search_by_author(self, author: str) -> list[Book]:
        book_list = list()
        if not author:
            return book_list
        for book in self.books.values():
            if author.lower() == book.author.lower():
                book_list.append(book)
        return book_list

    def borrow(self, member_id: str, isbn: str) -> bool:    
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        if not member or not book:
            return False
        if not member.can_borrow():
            return False
        if member.has_borrowed(book):
            return False
        copy = book.borrow_copy(member)
        if not copy:
            return False
        member.borrow_copy(copy)
        return True
    
    def return_book(self, copy: BookCopy, member: Member) -> bool:
        if not member or not copy:
            return False
        member.return_copy(copy)
        copy.book.return_copy(copy)
        return True
    
    def waitlist(self, title: Book, member:Member) -> Waitlist_Outcomes:
        if not member or not title:
            return Waitlist_Outcomes.ERROR
        if not member.waitlist_eligibility():
            return Waitlist_Outcomes.MEMBER_INELIGIBLE
        waitlist_result = title.add_member_to_waitlist(member)
        if waitlist_result == Waitlist_Outcomes.SUCCESS:
            member.add_title_to_waitlist(title)
        return waitlist_result

    def remove_copy_from_circulation(self, copy: BookCopy, reason: Book_State):
        copy.book.remove_from_circulation(copy, reason)