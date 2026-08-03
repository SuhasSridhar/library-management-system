from Members.Member import Member
from repositories.interfaces import MemberRepository

class InMemoryMemberRepository(MemberRepository):
    def __init__(self) -> None:
        self.members: dict[str, Member] = {}

    def add_member(self, member: Member) -> None:
        self.members[member.member_id] = member

    def get_member(self, member_id: str) -> Member | None:
        return self.members.get(member_id)

    def remove_member(self, member_id: str) -> None:
        try:
            del self.members[member_id]
        except KeyError:
            return