from Members.Member import Member


class MemberRepository:
    def __init__(self) -> None:
        self.members = {}

    def add_member(self, member: Member) -> Member | None:
        if not member:
            return
        self.members[member.member_id] = member

    def get_member(self, member_id: str) -> Member:
        return self.members.get(member_id)

    def remove_member(self, member_id: str) -> None:
        try:
            del self.members[member_id]
        except KeyError:
            return