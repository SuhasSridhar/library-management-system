from enums import Member_Type


class Member:
    def __init__(self, member_id: str, name: str, member_type: Member_Type) -> None:
        self.member_id = member_id
        self.name = name
        self.member_type = member_type
