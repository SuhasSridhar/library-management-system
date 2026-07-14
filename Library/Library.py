# Resposibility:
# Represents a single library branch.
# Owns the catalog of books and the registered members.
# Coordinates high-level workflows such as checkout and return.

from Members.Member import Member
from Inventory.Book import Book
from Inventory.BookCopy import BookCopy

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
    
    def add_book(self, title: str, author: str, ISBN: str, copies: list[str]) -> Book:
        # Add a title and a few copies for the same
        book = Book(
            title,
            author,
            ISBN
        )

        self.books[ISBN] = book

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
        copy.return_copy()
        return True