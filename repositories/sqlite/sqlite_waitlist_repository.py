from datetime import UTC, datetime

from database.sqlite_database import SQLiteDatabase
from enums import Member_Type, Waitlist_Outcomes
from Members.Member import Member
from repositories.interfaces import WaitListRepository


class SQLiteWaitListRepository(WaitListRepository):
    def __init__(self, database: SQLiteDatabase):
        self.connection = database.get_connection()

    def add_member_to_waitlist(self, isbn: str, member: Member) -> bool:
        if isbn is None or member is None:
            return False

        joined_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO WaitList(isbn, member_id, member_type, joined_at)
            VALUES(?, ?, ?, ?)
            """,
            (isbn, member.member_id, member.member_type.value, joined_at),
        )
        self.connection.commit()
        return True

    def get_next_eligible_member(self, isbn: str) -> str | None:

        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT member_id
            FROM WaitList
            WHERE isbn = ? 
            ORDER BY 
                CASE
                    WHEN member_type = ? THEN 0
                    ELSE 1
                END,
                joined_at ASC
            """,
            (isbn, Member_Type.FACULTY.value),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return str(row[0])

    def member_eligible_for_waitlist(
        self, member_id: str, isbn: str
    ) -> Waitlist_Outcomes:

        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(isbn)
            FROM WaitList
            WHERE member_id = ?
            """,
            (member_id,),
        )

        row = cursor.fetchone()

        if row[0] >= 2:
            return Waitlist_Outcomes.MEMBER_INELIGIBLE

        cursor.execute(
            """ 
            SELECT member_id
            FROM WaitList
            WHERE member_id = ? AND isbn = ?
            """,
            (
                member_id,
                isbn,
            ),
        )

        new_row = cursor.fetchone()

        if new_row is not None:
            return Waitlist_Outcomes.ALREADY_WAITING

        return Waitlist_Outcomes.SUCCESS
