from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from enums import Book_State, Waitlist_Outcomes
from Library.Library import Library

from .dependencies import get_library
from .schemas import BookCreate, BookResponse, MemberCreate, MemberResponse

router = APIRouter()


@router.get("/books/{isbn}", response_model=BookResponse)
def find_book(isbn: str, library: Library = Depends(get_library)) -> BookResponse:

    found_book = library.find_book(isbn)

    if found_book is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "BOOK_NOT_FOUND",
                "message": "The requested book does not exist.",
                "isbn": isbn,
            },
        )

    book_response = BookResponse(
        isbn=found_book.isbn,
        title=found_book.title,
        author=found_book.author,
    )

    return book_response


@router.get("/books", response_model=list[BookResponse])
def search_for_books(
    title: str | None = None,
    author: str | None = None,
    library: Library = Depends(get_library),
) -> list[BookResponse]:

    found_books = []
    if title:
        found_books = library.search_by_title(title)
    elif author:
        found_books = library.search_by_author(author)
    else:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "MISSING_SEARCH_VALUES",
                "message": "Search values are required to search books based on author or title.",
            },
        )

    if found_books is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "BOOK_NOT_FOUND",
                "message": "The requested book does not exist.",
                "title": title,
                "author": author,
            },
        )

    book_list: list[BookResponse] = []
    for book in found_books:
        book_response = BookResponse(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
        )
        book_list.append(book_response)

    return book_list


@router.get("/members/{member_id}", response_model=MemberResponse)
def find_member(
    member_id: str, library: Library = Depends(get_library)
) -> MemberResponse:
    found_member = library.find_member(member_id)
    if found_member is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "MEMBER_NOT_FOUND",
                "message": "The requested member does not exist.",
                "member_id": member_id,
            },
        )

    member_response = MemberResponse(
        member_id=found_member.member_id,
        name=found_member.name,
        member_type=found_member.member_type,
    )
    return member_response


@router.post("/members", response_model=MemberResponse, status_code=201)
def create_member(
    member: MemberCreate, library: Library = Depends(get_library)
) -> MemberResponse:
    created_member = library.add_member(
        member.member_id,
        member.name,
        member.member_type,
    )

    return MemberResponse(
        member_id=created_member.member_id,
        name=created_member.name,
        member_type=created_member.member_type,
    )


@router.post("/books", response_model=BookResponse, status_code=201)
def create_book(
    book: BookCreate, library: Library = Depends(get_library)
) -> BookResponse:
    created_book = library.add_book(
        book.title,
        book.author,
        book.isbn,
        book.copies,
    )

    return BookResponse(
        isbn=created_book.isbn, title=created_book.title, author=created_book.author
    )


@router.post("/return_copy", status_code=200)
def return_copy(
    copy_id: str, library: Library = Depends(get_library)
) -> dict[str, Any]:
    if not library.return_book(copy_id):
        raise HTTPException(
            status_code=404,
            detail={
                "error": "BOOK_RETURN_FAILED",
                "message": "The return of the book failed.",
                "copy_id": copy_id,
            },
        )
    else:
        return {"message": "Book copy returned successfully."}


@router.post("/borrow_copy/{isbn}", status_code=200)
def borrow_copy(
    member_id: str, isbn: str, library: Library = Depends(get_library)
) -> dict[str, Any]:
    if not library.borrow(member_id, isbn):
        raise HTTPException(
            status_code=404,
            detail={
                "error": "BORROW_FAILED",
                "message": "The book could not be borrowed by the requested member.",
                "member_id": member_id,
                "isbn": isbn,
            },
        )
    else:
        return {"message": "Borrowing the book was successful."}


@router.post("/waitlist", status_code=200)
def waitlist(
    isbn: str, member_id: str, library: Library = Depends(get_library)
) -> dict[str, Any]:
    outcome = library.waitlist(isbn, member_id)
    if outcome == Waitlist_Outcomes.ALREADY_WAITING:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "WAITLIST_FAILED",
                "message": "The requested member is already present in the Waitlist for the requested book.",
                "member_id": member_id,
                "isbn": isbn,
            },
        )
    elif outcome == Waitlist_Outcomes.MEMBER_INELIGIBLE:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "MEMBER_INELIGIBLE",
                "message": "The requested member is not eligible to be included in the Waitlist.",
                "member_id": member_id,
                "isbn": isbn,
            },
        )
    elif outcome == Waitlist_Outcomes.ERROR:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "WAITLIST_FAILED",
                "message": "Adding the member to the waitlist failed for the requested book.",
                "member_id": member_id,
                "isbn": isbn,
            },
        )
    else:
        return {"message": "Member added to the Waitlist Successfully"}


@router.delete("/copies/{copy_id}", status_code=200)
def remove_copy_from_circulation(
    copy_id: str, reason: Book_State, library: Library = Depends(get_library)
) -> dict[str, Any]:
    library.remove_copy_from_circulation(copy_id, reason)
    return {"message": "Copy removed from circulation Successfully."}


@router.delete("/members/{member_id}", status_code=200)
def remove_member(
    member_id: str, library: Library = Depends(get_library)
) -> dict[str, Any]:
    library.remove_member(member_id)
    return {"message": "Member removed from circulation Successfully."}
