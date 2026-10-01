from enum import Enum


class Book_State(Enum):
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    RESERVED = "RESERVED"
    REMOVED = "REMOVED"
    DAMAGED = "DAMAGED"
    LOST = "LOST"


class Member_Type(Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"


class Waitlist_Outcomes(Enum):
    SUCCESS = "Success"
    ALREADY_WAITING = "Already Waiting"
    MEMBER_INELIGIBLE = "Member Ineligible"
    ERROR = "Input Error"
