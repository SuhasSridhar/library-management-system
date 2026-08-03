# Resposibility:
# Represents a single library branch.
# Owns the catalog of books and the registered members.
# Coordinates high-level workflows such as checkout and return.

from enums import Book_State, Waitlist_Outcomes, Member_Type
from Inventory.Book import Book
from Inventory.BookCopy import BookCopy
from Members.Member import Member
from repositories.interfaces import BookRepository, MemberRepository


class Library:
    def __init__(self, member_repo: MemberRepository, books_repo: BookRepository) -> None:
        self.member_repository = member_repo
        self.book_repository = books_repo

    def add_member(self, member_id: str, name: str, member_type: Member_Type) -> Member:
        # Add students
        member = Member(
            member_id,
            name,
            member_type
        )
        self.member_repository.add_member(member)
        return member
    
    def add_book(self, title: str, author: str, isbn: str, copies: list[str]) -> Book:
        # Add a title and a few copies for the same
        book = Book(
            title,
            author,
            isbn
        )

        for copy in copies:
            book.add_copy(copy)

        self.book_repository.add_book(book)

        return book
    
    def find_member(self, member_id: str) -> Member | None:
        if not member_id:
            return None
        return self.member_repository.get_member(member_id)
    
    def find_book(self, isbn: str) -> Book | None:
        if not isbn:
            return None
        return self.book_repository.get_book(isbn)

    def search_by_title(self, title: str) -> list[Book]:
        book_list: list[Book] = []
        if not title:
            return book_list
        book_list = self.book_repository.search_by_title(title)
        return book_list

    def search_by_author(self, author: str) -> list[Book]:
        book_list: list[Book] = []
        if not author:
            return book_list
        book_list = self.book_repository.search_by_author(author)
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

    def remove_copy_from_circulation(self, copy: BookCopy, reason: Book_State) -> None:
        copy.book.remove_from_circulation(copy, reason)

    def remove_member(self, member_id: str) -> None:
        if not member_id:
            return
        return self.member_repository.remove_member(member_id)