from datetime import UTC, datetime, timedelta

from database.sqlite_database import SQLiteDatabase
from enums import Book_State
from Inventory.BookCopy import BookCopy
from repositories.interfaces import BookCopyRepository


class SQLiteBookCopyRepository(BookCopyRepository):
    def __init__(self, database: SQLiteDatabase):
        self.connection = database.get_connection()

    def add_copy(self, copy: BookCopy) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO BookCopy(copy_id, isbn, status)
            VALUES(?, ?, ?)
            """,
            (
                copy.copy_id,
                copy.isbn,
                copy.status.value,
            ),
        )
        self.connection.commit()

    def eligible_to_borrow(self, member_id: str, isbn: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT copy_id
            FROM BookCopy
            WHERE isbn = ? AND borrower_member_id = ?
            """,
            (
                isbn,
                member_id,
            ),
        )
        row = cursor.fetchone()
        if row is not None:
            return False

        cursor.execute(
            """
            SELECT COUNT(copy_id)
            FROM BookCopy
            WHERE borrower_member_id = ?
            """,
            (member_id,),
        )
        row = cursor.fetchone()
        return int(row[0]) < 2

    def fetch_available_copy(self, isbn: str) -> BookCopy | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT copy_id, isbn, status
            FROM BookCopy
            WHERE isbn = ?
              AND borrower_member_id IS NULL
              AND status = ?
            """,
            (
                isbn,
                Book_State.AVAILABLE.value,
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        copy = BookCopy(
            barcode=row[0],
            isbn=row[1],
            status=Book_State(row[2]),
        )
        return copy

    def borrow_copy(self, member_id: str, copy: BookCopy) -> bool:
        today = datetime.now(UTC).date()
        due_date = today + timedelta(days=10)

        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE BookCopy
            SET
                borrower_member_id = ?,
                borrowed_date = ?,
                due_date = ?,
                status = ?
            WHERE copy_id = ?
            """,
            (
                member_id,
                today,
                due_date,
                Book_State.BORROWED.value,
                copy.copy_id,
            ),
        )
        self.connection.commit()
        return cursor.rowcount == 1

    def get_copy(self, barcode: str) -> BookCopy | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT copy_id, isbn, status
            FROM BookCopy
            WHERE copy_id = ?
            """,
            (barcode,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        copy = BookCopy(
            barcode=row[0],
            isbn=row[1],
            status=Book_State(row[2]),
        )
        return copy

    def return_copy(self, copy: BookCopy) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE BookCopy
            SET
                status = ?,
                borrower_member_id = NULL,
                due_date = NULL,
                borrowed_date = NULL,
                reservation_member_id = NULL,
                reservation_expiry = NULL
            WHERE copy_id = ?
            """,
            (
                Book_State.AVAILABLE.value,
                copy.copy_id,
            ),
        )
        self.connection.commit()

    def reserve_copy_for_waiting_member(
        self,
        barcode: str,
        member_id: str,
    ) -> bool:
        today = datetime.now(UTC).date()
        reservation_due = today + timedelta(days=1)

        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE BookCopy
            SET
                status = ?,
                borrower_member_id = NULL,
                due_date = NULL,
                borrowed_date = NULL,
                reservation_member_id = ?,
                reservation_expiry = ?
            WHERE copy_id = ?
            """,
            (
                Book_State.RESERVED.value,
                member_id,
                reservation_due,
                barcode,
            ),
        )
        self.connection.commit()
        return cursor.rowcount == 1

    def remove_from_circulation(
        self,
        copy: BookCopy,
        reason: Book_State,
    ) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE BookCopy
            SET
                status = ?,
                borrower_member_id = NULL,
                borrowed_date = NULL,
                due_date = NULL,
                reservation_member_id = NULL,
                reservation_expiry = NULL
            WHERE copy_id = ?
            """,
            (
                reason.value,
                copy.copy_id,
            ),
        )

        self.connection.commit()
