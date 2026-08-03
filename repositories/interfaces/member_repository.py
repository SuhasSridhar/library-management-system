from abc import ABC, abstractmethod
from Members.Member import Member

class MemberRepository(ABC):

    @abstractmethod
    def add_member(self, member: Member) -> None:
        ...

    @abstractmethod
    def get_member(self, member_id: str) -> Member | None:
        ...

    @abstractmethod
    def remove_member(self, member_id: str) -> None:
        ...