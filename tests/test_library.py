import pytest
from datetime import date, timedelta
from repositories import BookRepository
from repositories import MemberRepository
from enums import Book_State
from Library.Library import Library


@pytest.fixture
def library() -> Library:
    member_repo = MemberRepository()
    books_repo = BookRepository()
    library = Library(member_repo, books_repo)

    library.add_member(
        member_id="STU001",
        name="Suhas",
        member_type="Student"
    )

    library.add_book(
        title="Clean Architecture",
        author="Robert C. Martin",
        isbn="ISBN001",
        copies=[
            "BC001",
            "BC002",
            "BC003"
        ]
    )

    return library


def test_successful_checkout(library: Library) -> None:
    success = library.borrow("STU001", "ISBN001")

    assert success is True

    member = library.find_member("STU001")
    book = library.find_book("ISBN001")

    assert len(member.borrowed_books) == 1

    borrowed_copy = member.borrowed_books[0]

    assert borrowed_copy.borrower == member
    assert borrowed_copy.state == Book_State.BORROWED
    assert borrowed_copy.due_date is not None

    available = [
        copy
        for copy in book.copies.values()
        if copy.state == Book_State.AVAILABLE
    ]

    assert len(available) == 2


def test_unknown_member_cannot_checkout(library: Library) -> None:
    assert library.borrow("UNKNOWN", "ISBN001") is False


def test_unknown_book_cannot_checkout(library: Library) -> None:
    assert library.borrow("STU001", "UNKNOWN") is False


def test_member_cannot_borrow_same_title_twice(library: Library) -> None:
    assert library.borrow("STU001", "ISBN001") is True

    assert library.borrow("STU001", "ISBN001") is False

    member = library.find_member("STU001")

    assert len(member.borrowed_books) == 1


def test_member_cannot_exceed_limit(library: Library) -> None:
    library.add_book(
        "Book2",
        "Author",
        "ISBN002",
        ["BC004"]
    )

    library.add_book(
        "Book3",
        "Author",
        "ISBN003",
        ["BC005"]
    )

    library.add_book(
        "Book4",
        "Author",
        "ISBN004",
        ["BC006"]
    )

    assert library.borrow("STU001", "ISBN001")
    assert library.borrow("STU001", "ISBN002")
    assert library.borrow("STU001", "ISBN003")

    assert library.borrow("STU001", "ISBN004") is False

    member = library.find_member("STU001")

    assert len(member.borrowed_books) == 3


def test_no_available_copy(library: Library) -> None:
    library.add_member(
        "STU002",
        "Alice",
        "Student"
    )

    library.add_member(
        "STU003",
        "Bob",
        "Student"
    )

    assert library.borrow("STU001", "ISBN001")
    assert library.borrow("STU002", "ISBN001")
    assert library.borrow("STU003", "ISBN001")

    library.add_member(
        "STU004",
        "David",
        "Student"
    )

    assert library.borrow("STU004", "ISBN001") is False


def test_return_book(library: Library) -> None:
    library.borrow("STU001", "ISBN001")

    member = library.find_member("STU001")
    copy = member.borrowed_books[0]

    assert library.return_book(copy, member)

    assert len(member.borrowed_books) == 0

    assert copy.borrower is None
    assert copy.state == Book_State.AVAILABLE
    assert copy.due_date is None


def test_return_invalid_arguments(library: Library) -> None:
    member = library.find_member("STU001")

    assert library.return_book(None, member) is False
    assert library.return_book(None, None) is False

def test_member_can_join_waitlist(library: Library) -> None:
    library.add_member("STU002", "Alice", "Student")
    library.add_member("STU003", "Bob", "Student")
    library.add_member("STU004", "David", "Student")

    assert library.borrow("STU001", "ISBN001")
    assert library.borrow("STU002", "ISBN001")
    assert library.borrow("STU003", "ISBN001")

    member = library.find_member("STU004")
    book = library.find_book("ISBN001")

    result = library.waitlist(book, member)

    assert result.name == "SUCCESS"
    assert member.waiting_lists == [book]
    assert len(book.waiting_list) == 1

def test_member_cannot_join_waitlist_twice(library: Library) -> None:
    library.add_member("STU002", "Alice", "Student")
    library.add_member("STU003", "Bob", "Student")
    library.add_member("STU004", "David", "Student")

    library.borrow("STU001", "ISBN001")
    library.borrow("STU002", "ISBN001")
    library.borrow("STU003", "ISBN001")

    member = library.find_member("STU004")
    book = library.find_book("ISBN001")

    assert library.waitlist(book, member).name == "SUCCESS"
    assert library.waitlist(book, member).name == "ALREADY_WAITING"

    assert len(book.waiting_list) == 1

def test_returned_copy_reserved_for_waiting_member(library: Library) -> None:
    library.add_member("STU002", "Alice", "Student")
    library.add_member("STU003", "Bob", "Student")
    library.add_member("STU004", "David", "Student")

    library.borrow("STU001", "ISBN001")
    library.borrow("STU002", "ISBN001")
    library.borrow("STU003", "ISBN001")

    waiting_member = library.find_member("STU004")
    book = library.find_book("ISBN001")

    library.waitlist(book, waiting_member)

    borrower = library.find_member("STU001")
    copy = borrower.borrowed_books[0]

    library.return_book(copy, borrower)

    assert copy.state == Book_State.RESERVED
    assert copy.reservation == waiting_member
    assert copy in waiting_member.active_reservations
    assert book not in waiting_member.waiting_lists

def test_expired_reservation_reassigned(library: Library) -> None:
    library.add_member("STU002", "Alice", "Student")
    library.add_member("STU003", "Bob", "Student")
    library.add_member("STU004", "David", "Student")
    library.add_member("STU005", "Charlie", "Student")

    library.borrow("STU001", "ISBN001")
    library.borrow("STU002", "ISBN001")
    library.borrow("STU003", "ISBN001")

    book = library.find_book("ISBN001")

    david = library.find_member("STU004")
    charlie = library.find_member("STU005")

    library.waitlist(book, david)
    library.waitlist(book, charlie)

    borrower = library.find_member("STU001")
    copy = borrower.borrowed_books[0]

    library.return_book(copy, borrower)

    copy.reservation_due = date.today() - timedelta(days=1)

    book.expired_validation()

    assert copy.reservation == charlie
    assert copy in charlie.active_reservations
    assert copy not in david.active_reservations

def test_member_with_overdue_book_cannot_borrow(library: Library) -> None:
    library.add_book(
        "Book2",
        "Author",
        "ISBN002",
        ["BC010"]
    )

    library.borrow("STU001", "ISBN001")

    member = library.find_member("STU001")

    copy = member.borrowed_books[0]

    copy.due_date = date.today() - timedelta(days=1)

    assert library.borrow("STU001", "ISBN002") is False

def test_returning_overdue_book_restores_borrowing(library: Library) -> None:
    library.add_book(
        "Book2",
        "Author",
        "ISBN002",
        ["BC010"]
    )

    library.borrow("STU001", "ISBN001")

    member = library.find_member("STU001")
    copy = member.borrowed_books[0]

    copy.due_date = date.today() - timedelta(days=1)

    assert library.borrow("STU001", "ISBN002") is False

    library.return_book(copy, member)

    assert library.borrow("STU001", "ISBN002") is True

def test_damaged_copy_cannot_be_borrowed(library: Library) -> None:
    book = library.find_book("ISBN001")
    copy = book.copies["BC001"]

    library.remove_copy_from_circulation(copy, Book_State.DAMAGED)

    library.add_member("STU002", "Alice", "Student")

    assert library.borrow("STU002", "ISBN001") is True
    assert copy.barcode not in book.copies

def test_lost_copy_cannot_be_borrowed(library: Library) -> None:
    book = library.find_book("ISBN001")
    copy = book.copies["BC001"]

    library.remove_copy_from_circulation(copy, Book_State.LOST)

    library.add_member("STU002", "Alice", "Student")

    assert library.borrow("STU002", "ISBN001") is True
    assert copy.barcode not in book.copies

def test_removed_copy_cannot_be_borrowed(library: Library) -> None:
    book = library.find_book("ISBN001")
    copy = book.copies["BC001"]

    library.remove_copy_from_circulation(copy, Book_State.REMOVED)

    library.add_member("STU002", "Alice", "Student")

    assert library.borrow("STU002", "ISBN001") is True
    assert copy.barcode not in book.copies

def test_removed_copy_moves_to_archive(library: Library) -> None:
    book = library.find_book("ISBN001")
    copy = book.copies["BC001"]

    library.remove_copy_from_circulation(copy, Book_State.REMOVED)

    assert "BC001" not in book.copies
    assert "BC001" in book.archived_books
    assert book.archived_books["BC001"] == copy

def test_removing_one_copy_keeps_other_copies_available(library: Library) -> None:
    book = library.find_book("ISBN001")
    copy = book.copies["BC001"]

    library.remove_copy_from_circulation(copy, Book_State.DAMAGED)

    available = [
        c
        for c in book.copies.values()
        if c.state == Book_State.AVAILABLE
    ]

    assert len(available) == 2

def test_available_inventory_decreases_after_retirement(library: Library) -> None:
    book = library.find_book("ISBN001")

    assert len(book.copies) == 3

    copy = book.copies["BC001"]

    library.remove_copy_from_circulation(copy, Book_State.REMOVED)

    assert len(book.copies) == 2

def test_borrowed_copy_removed_updates_member(library: Library) -> None:
    assert library.borrow("STU001", "ISBN001")

    member = library.find_member("STU001")
    copy = member.borrowed_books[0]

    library.remove_copy_from_circulation(copy, Book_State.LOST)

    assert len(member.borrowed_books) == 0
    assert copy.borrower is None
    assert copy.due_date is None

def test_reserved_copy_removed_updates_member(library: Library) -> None:
    library.add_member("STU002", "Alice", "Student")
    library.add_member("STU003", "Bob", "Student")
    library.add_member("STU004", "David", "Student")

    library.borrow("STU001", "ISBN001")
    library.borrow("STU002", "ISBN001")
    library.borrow("STU003", "ISBN001")

    waiting_member = library.find_member("STU004")
    book = library.find_book("ISBN001")

    library.waitlist(book, waiting_member)

    borrower = library.find_member("STU001")
    reserved_copy = borrower.borrowed_books[0]

    library.return_book(reserved_copy, borrower)

    assert reserved_copy in waiting_member.active_reservations

    library.remove_copy_from_circulation(
        reserved_copy,
        Book_State.DAMAGED
    )

    assert reserved_copy not in waiting_member.active_reservations
    assert reserved_copy.reservation is None

def test_find_book_by_isbn(library: Library) -> None:
    book = library.find_book("ISBN001")

    assert book is not None
    assert book.isbn == "ISBN001"

def test_find_unknown_book_returns_none(library: Library) -> None:
    assert library.find_book("UNKNOWN") is None

def test_search_by_title_returns_matching_books(library: Library) -> None:
    books = library.search_by_title("Clean Architecture")

    assert len(books) == 1
    assert books[0].isbn == "ISBN001"

def test_search_by_unknown_title_returns_empty_list(library: Library) -> None:
    books = library.search_by_title("Some Random Book")

    assert books == []

def test_search_by_author_returns_matching_books(library: Library) -> None:
    books = library.search_by_author("Robert C. Martin")

    assert len(books) == 1
    assert books[0].isbn == "ISBN001"

def test_search_by_unknown_author_returns_empty_list(library: Library) -> None:
    books = library.search_by_author("Unknown Author")

    assert books == []

def test_search_returns_all_books_for_author(library: Library) -> None:
    library.add_book(
        "Clean Code",
        "Robert C. Martin",
        "ISBN002",
        ["BC004"]
    )

    books = library.search_by_author("Robert C. Martin")

    assert len(books) == 2

def test_search_returns_all_books_with_same_title(library: Library) -> None:
    library.add_book(
        "Clean Architecture",
        "Robert C. Martin",
        "ISBN002",
        ["BC004"]
    )

    books = library.search_by_title("Clean Architecture")

    assert len(books) == 2

def test_search_by_title_is_case_insensitive(library: Library) -> None:
    books = library.search_by_title("clean architecture")

    assert len(books) == 1

def test_available_copy_count_updates_after_checkout(library: Library) -> None:
    book = library.find_book("ISBN001")

    assert book.check_available_copies() == 3

    library.borrow("STU001", "ISBN001")

    assert book.check_available_copies() == 2

def test_available_copy_count_updates_after_return(library: Library) -> None:
    book = library.find_book("ISBN001")

    library.borrow("STU001", "ISBN001")

    member = library.find_member("STU001")
    copy = member.borrowed_books[0]

    library.return_book(copy, member)

    assert book.check_available_copies() == 3