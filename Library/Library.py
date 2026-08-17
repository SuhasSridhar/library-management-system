# Resposibility:
# Represents a single library branch.
# Owns the catalog of books and the registered members.
# Coordinates high-level workflows such as checkout and return.

from enums import Book_State, Member_Type, Waitlist_Outcomes
from Inventory.Book import Book
from Inventory.BookCopy import BookCopy
from Members.Member import Member
from repositories.interfaces import (
    BookCopyRepository,
    BookRepository,
    MemberRepository,
    WaitListRepository,
)


class Library:
    def __init__(self, member_repo: MemberRepository, books_repo: BookRepository, books_copy_repo: BookCopyRepository, waitlist_repo: WaitListRepository) -> None:
        self.member_repository = member_repo
        self.book_repository = books_repo
        self.book_copy_repository = books_copy_repo
        self.waitlist_repository = waitlist_repo

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

        # Method to add book copy 
        for copy in copies:
            book_copy = BookCopy(isbn, copy)
            self.book_copy_repository.add_copy(book_copy)

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
        if not member:
            return False
        if not book:
            return False
        if not self.book_copy_repository.eligible_to_borrow(member_id, isbn):
            return False
        copy = self.book_copy_repository.fetch_available_copy(isbn)
        if not copy:
            return False
        return self.book_copy_repository.borrow_copy(member_id, copy) # borrow happens in the copy, Book copy holds the copy and it does have an ISBN stored as a field.

    def return_book(self, copy: BookCopy, member: Member) -> bool:
        if not member or not copy:
            return False
        self.book_copy_repository.return_copy(copy)
        waiting_member_id = self.waitlist_repository.get_next_eligible_member(copy.isbn)
        if not waiting_member_id:
            return True
        if self.book_copy_repository.reserve_copy_for_waiting_member(copy.copy_id, waiting_member_id):
            return True
        return False

    # Method to add a member to Waitlist.
    def waitlist(self, title: Book, member: Member) -> Waitlist_Outcomes:
        if not title or not member:
            return Waitlist_Outcomes.ERROR
        waitlist_outcome = self.waitlist_repository.member_eligible_for_waitlist(member.member_id, title.isbn)
        if waitlist_outcome == Waitlist_Outcomes.SUCCESS:
            waitlist_result = self.waitlist_repository.add_member_to_waitlist(title.isbn, member)
            return Waitlist_Outcomes.SUCCESS if waitlist_result is True else Waitlist_Outcomes.ERROR
        return waitlist_outcome

    def remove_copy_from_circulation(self, copy: BookCopy, reason: Book_State) -> None:
        self.book_copy_repository.remove_from_circulation(copy, reason)

    def remove_member(self, member_id: str) -> None:
        if not member_id:
            return
        return self.member_repository.remove_member(member_id)