from abc import ABC, abstractmethod
from Members.Member import Member
from enums import Waitlist_Outcomes

class WaitListRepository(ABC):

    @abstractmethod
    def add_member_to_waitlist(self, isbn: str, member: Member) -> bool:
        ...

    @abstractmethod
    def get_next_eligible_member(self, isbn: str) -> str | None:
        ...

    @abstractmethod
    def member_eligible_for_waitlist(self, member_id: str, isbn: str) -> Waitlist_Outcomes:
        ...