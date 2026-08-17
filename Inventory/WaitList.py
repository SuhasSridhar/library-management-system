from enums import Member_Type

class WaitList:
    def __init__ (self, isbn: str, member_id: str, position: Member_Type, joined_at: str) -> None:
        self.isbn = isbn
        self.member_id = member_id
        self.position = position
        self.joined_at = joined_at