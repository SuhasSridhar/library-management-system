from collections import deque

from enums import Member_Type, Waitlist_Outcomes
from Inventory.WaitList import WaitList
from Members.Member import Member
from repositories.interfaces import WaitListRepository


class InMemoryWaitListRepository(WaitListRepository):

    def __init__(self) -> None:
        self.waitlist_records: dict[str, deque[WaitList]] = {}

    def add_member_to_waitlist(self, isbn: str, member: Member) -> bool:
        if isbn is None or member is None:
            return False
        waitlist = WaitList(isbn, member.member_id, member.member_type, '')
        if isbn not in self.waitlist_records:
            self.waitlist_records[isbn] = deque()
        if member.member_type == Member_Type.FACULTY:
            self.waitlist_records[isbn].appendleft(waitlist)
        else :
            self.waitlist_records[isbn].append(waitlist)
        return True

    def get_next_eligible_member(self, isbn: str) -> str | None:
        waitlist = self.waitlist_records.get(isbn)
        if waitlist is None:
            return None
        waitlist_member = waitlist.popleft()
        return waitlist_member.member_id

    def member_eligible_for_waitlist(self, member_id: str, isbn: str) -> Waitlist_Outcomes:
        count = 0
        for waitlist in self.waitlist_records.values():
            for rec in waitlist:
                if rec.member_id == member_id:
                    count += 1
                    if rec.isbn == isbn:
                        return Waitlist_Outcomes.ALREADY_WAITING
                if count == 2:
                    return Waitlist_Outcomes.MEMBER_INELIGIBLE
        return Waitlist_Outcomes.SUCCESS