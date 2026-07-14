import pytest

from Library.Library import Library
from enums import Book_State


@pytest.fixture
def library():
    library = Library()

    library.add_member(
        member_id="STU001",
        name="Suhas",
        member_type="Student"
    )

    library.add_book(
        title="Clean Architecture",
        author="Robert C. Martin",
        ISBN="ISBN001",
        copies=[
            "BC001",
            "BC002",
            "BC003"
        ]
    )

    return library


def test_successful_checkout(library):
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


def test_unknown_member_cannot_checkout(library):
    assert library.borrow("UNKNOWN", "ISBN001") is False


def test_unknown_book_cannot_checkout(library):
    assert library.borrow("STU001", "UNKNOWN") is False


def test_member_cannot_borrow_same_title_twice(library):
    assert library.borrow("STU001", "ISBN001") is True

    assert library.borrow("STU001", "ISBN001") is False

    member = library.find_member("STU001")

    assert len(member.borrowed_books) == 1


def test_member_cannot_exceed_limit(library):
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


def test_no_available_copy(library):
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


def test_return_book(library):
    library.borrow("STU001", "ISBN001")

    member = library.find_member("STU001")
    copy = member.borrowed_books[0]

    assert library.return_book(copy, member)

    assert len(member.borrowed_books) == 0

    assert copy.borrower is None
    assert copy.state == Book_State.AVAILABLE
    assert copy.due_date is None


def test_return_invalid_arguments(library):
    member = library.find_member("STU001")

    assert library.return_book(None, member) is False
    assert library.return_book(None, None) is False