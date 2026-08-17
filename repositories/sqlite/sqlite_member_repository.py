from database.sqlite_database import SQLiteDatabase
from enums import Member_Type
from Members.Member import Member
from repositories.interfaces import MemberRepository


class SQLiteMemberRepository(MemberRepository):
    def __init__(self, database: SQLiteDatabase):
        self.connection = database.get_connection()

    def add_member(self, member: Member) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO Member(member_id, name, member_type)
            VALUES(?, ?, ?)
            """,
            (member.member_id, member.name, member.member_type.value),
        )
        self.connection.commit()

    def get_member(self, member_id: str) -> Member | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT member_id, name, member_type
            FROM Member
            WHERE member_id = ?
            """,
            (member_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Member(member_id=row[0], name=row[1], member_type=Member_Type(row[2]))

    def remove_member(self, member_id: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            DELETE 
            FROM Member 
            WHERE member_id = ?
            """,
            (member_id),
        )

        self.connection.commit()
