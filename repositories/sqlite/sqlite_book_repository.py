from database.sqlite_database import SQLiteDatabase
from Inventory.Book import Book
from repositories.interfaces import BookRepository


class SQLiteBookRepository(BookRepository):
    
    def __init__(self, database: SQLiteDatabase):
        self.connection = database.get_connection()

    def add_book(self, book: Book) -> None:
        if not book:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO Book(isbn, title, author)
            VALUES(?, ?, ?)
            """,
            (
                book.isbn,
                book.title,
                book.author,
            ),
        )
        self.connection.commit()

    def get_book(self, isbn: str) -> Book | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """ 
            SELECT isbn, title, author
            FROM Book
            WHERE isbn = ?
            """,
            (
                isbn,
            )
        )

        row = cursor.fetchone()

        if row is None:
            return None
        
        return Book(
            isbn=row[0],
            title=row[1],
            author=row[2]
        )

    def search_by_author(self, author: str) -> list[Book]:
        book_list: list[Book] = []

        cursor = self.connection.cursor()
        cursor.execute(
            """ 
            SELECT isbn, title, author
            FROM Book
            WHERE author = ?
            """,
            (
                author,
            )
        )

        rows = cursor.fetchall()

        for row in rows:
            book_list.append(Book(
                isbn=row[0],
                title=row[1],
                author=row[2]
            ))

        return book_list

    def search_by_title(self, title: str) -> list[Book]:
        book_list: list[Book] = []

        cursor = self.connection.cursor()
        cursor.execute(
            """ 
            SELECT isbn, title, author
            FROM Book
            WHERE title = ?
            """,
            (
                title,
            )
        )

        rows = cursor.fetchall()

        for row in rows:
            book_list.append(Book(
                isbn=row[0],
                title=row[1],
                author=row[2]
            ))

        return book_list