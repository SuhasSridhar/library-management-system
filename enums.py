from enum import Enum

class Book_State(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    RESERVED = "Reserved"
    REMOVED = "Removed"
    DAMAGED = "Damaged"
    LOST = "Lost"

class Member_Type(Enum):
    STUDENT = "Student"
    FACULTY = "Faculty"

class Waitlist_Outcomes(Enum):
    SUCCESS = "Success"
    ALREADY_WAITING = "Already Waiting"
    MEMBER_INELIGIBLE = "Member Ineligible"
    ERROR = "Input Error"