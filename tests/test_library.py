import pytest

from enums import Book_State, Member_Type, Waitlist_Outcomes
from Library.Library import Library
from repositories.in_memory import (
    InMemoryBookCopyRepository,
    InMemoryBookRepository,
    InMemoryMemberRepository,
    InMemoryWaitListRepository,
)


@pytest.fixture
def library() -> Library:
    return Library(
        member_repo=InMemoryMemberRepository(),
        books_repo=InMemoryBookRepository(),
        books_copy_repo=InMemoryBookCopyRepository(),
        waitlist_repo=InMemoryWaitListRepository(),
    )


@pytest.fixture
def populated_library(library: Library) -> Library:
    library.add_member(
        "M001",
        "Alice",
        Member_Type.STUDENT,
    )
    library.add_member(
        "F001",
        "Dr. Emily",
        Member_Type.FACULTY,
    )

    library.add_book(
        "Clean Architecture",
        "Robert C. Martin",
        "ISBN001",
        ["C001", "C002"],
    )

    return library


def test_add_and_find_member(library: Library) -> None:
    member = library.add_member(
        "M001",
        "Alice",
        Member_Type.STUDENT,
    )

    found_member = library.find_member("M001")

    assert found_member is member
    assert found_member is not None
    assert found_member.member_id == "M001"
    assert found_member.name == "Alice"
    assert found_member.member_type == Member_Type.STUDENT


def test_find_nonexistent_member_returns_none(library: Library) -> None:
    assert library.find_member("INVALID") is None


def test_add_and_find_book(library: Library) -> None:
    book = library.add_book(
        "Clean Architecture",
        "Robert C. Martin",
        "ISBN001",
        ["C001", "C002"],
    )

    found_book = library.find_book("ISBN001")

    assert found_book is book
    assert found_book is not None
    assert found_book.isbn == "ISBN001"
    assert found_book.title == "Clean Architecture"
    assert found_book.author == "Robert C. Martin"


def test_find_nonexistent_book_returns_none(library: Library) -> None:
    assert library.find_book("INVALID") is None


def test_search_book_by_title(library: Library) -> None:
    library.add_book(
        "Clean Architecture",
        "Robert C. Martin",
        "ISBN001",
        ["C001"],
    )
    library.add_book(
        "Design Patterns",
        "Erich Gamma",
        "ISBN002",
        ["C002"],
    )

    results = library.search_by_title("Clean Architecture")

    assert len(results) == 1
    assert results[0].isbn == "ISBN001"


def test_search_book_by_author(library: Library) -> None:
    library.add_book(
        "Clean Architecture",
        "Robert C. Martin",
        "ISBN001",
        ["C001"],
    )
    library.add_book(
        "Design Patterns",
        "Erich Gamma",
        "ISBN002",
        ["C002"],
    )

    results = library.search_by_author("Robert C. Martin")

    assert len(results) == 1
    assert results[0].isbn == "ISBN001"


def test_search_with_empty_title_returns_empty_list(library: Library) -> None:
    assert library.search_by_title("") == []


def test_search_with_empty_author_returns_empty_list(library: Library) -> None:
    assert library.search_by_author("") == []


def test_successful_checkout(populated_library: Library) -> None:
    result = populated_library.borrow("M001", "ISBN001")

    assert result is True


def test_checkout_nonexistent_member(populated_library: Library) -> None:
    result = populated_library.borrow("INVALID", "ISBN001")

    assert result is False


def test_checkout_nonexistent_book(populated_library: Library) -> None:
    result = populated_library.borrow("M001", "INVALID")

    assert result is False


def test_checkout_same_book_twice_is_rejected(populated_library: Library) -> None:
    first_result = populated_library.borrow("M001", "ISBN001")
    second_result = populated_library.borrow("M001", "ISBN001")

    assert first_result is True
    assert second_result is False


def test_member_cannot_borrow_more_than_allowed(
    populated_library: Library,
) -> None:
    populated_library.add_book(
        "Book Two",
        "Author Two",
        "ISBN002",
        ["C003"],
    )
    populated_library.add_book(
        "Book Three",
        "Author Three",
        "ISBN003",
        ["C004"],
    )
    populated_library.add_book(
        "Book Four",
        "Author Four",
        "ISBN004",
        ["C005"],
    )

    assert populated_library.borrow("M001", "ISBN001") is True
    assert populated_library.borrow("M001", "ISBN002") is True
    assert populated_library.borrow("M001", "ISBN003") is True
    assert populated_library.borrow("M001", "ISBN004") is False


def test_return_book_makes_copy_available(
    populated_library: Library,
) -> None:
    populated_library.borrow("M001", "ISBN001")

    copy = populated_library.book_copy_repository.get_copy("C001")

    assert copy is not None

    member = populated_library.find_member("M001")
    if member is None:
        return
    result = populated_library.return_book(
        copy,
        member,
    )

    assert result is True
    assert copy.status == Book_State.AVAILABLE


def test_return_book_reserves_copy_for_waiting_member(
    populated_library: Library,
) -> None:
    populated_library.borrow("M001", "ISBN001")

    copy = populated_library.book_copy_repository.get_copy("C001")
    member = populated_library.find_member("F001")
    book = populated_library.find_book("ISBN001")

    assert copy is not None
    assert member is not None
    assert book is not None

    waitlist_result = populated_library.waitlist(
        book,
        member,
    )

    assert waitlist_result == Waitlist_Outcomes.SUCCESS

    result = populated_library.return_book(copy, member)

    assert result is True
    assert copy.status == Book_State.RESERVED
    assert copy.reservation_member_id == "F001"


def test_member_can_join_waitlist(populated_library: Library) -> None:
    book = populated_library.find_book("ISBN001")
    member = populated_library.find_member("M001")

    assert book is not None
    assert member is not None

    result = populated_library.waitlist(book, member)

    assert result == Waitlist_Outcomes.SUCCESS


def test_member_cannot_join_same_waitlist_twice(
    populated_library: Library,
) -> None:
    book = populated_library.find_book("ISBN001")
    member = populated_library.find_member("M001")

    assert book is not None
    assert member is not None

    first_result = populated_library.waitlist(book, member)
    second_result = populated_library.waitlist(book, member)

    assert first_result == Waitlist_Outcomes.SUCCESS
    assert second_result == Waitlist_Outcomes.ALREADY_WAITING


def test_remove_copy_from_circulation(
    populated_library: Library,
) -> None:
    copy = populated_library.book_copy_repository.get_copy("C001")

    assert copy is not None

    populated_library.remove_copy_from_circulation(
        copy,
        Book_State.REMOVED,
    )

    assert copy.status == Book_State.REMOVED


def test_remove_member(populated_library: Library) -> None:
    populated_library.remove_member("M001")

    assert populated_library.find_member("M001") is None