from enum import Enum

class Book_State(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    RESERVED = "Reserved"
    REMOVED = "Removed"

class Member_Type(Enum):
    STUDENT = "Student"
    FACULTY = "Faculty"