from database.sqlite_database import SQLiteDatabase
from Library.Library import Library
from repositories.sqlite.sqlite_book_copy_repository import SQLiteBookCopyRepository
from repositories.sqlite.sqlite_book_repository import SQLiteBookRepository
from repositories.sqlite.sqlite_member_repository import SQLiteMemberRepository
from repositories.sqlite.sqlite_waitlist_repository import SQLiteWaitListRepository


def main() -> None:
    database = SQLiteDatabase("library.db")

    book_repository = SQLiteBookRepository(database)
    book_copy_repository = SQLiteBookCopyRepository(database)
    member_repository = SQLiteMemberRepository(database)
    waitlist_repository = SQLiteWaitListRepository(database)

    library = Library(
        member_repo=member_repository,
        books_repo=book_repository,
        books_copy_repo=book_copy_repository,
        waitlist_repo=waitlist_repository,
    )

    _ = library


if __name__ == "__main__":
    main()