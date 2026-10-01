from pydantic import BaseModel

from enums import Member_Type


class BookResponse(BaseModel):
    isbn: str
    title: str
    author: str


class MemberCreate(BaseModel):
    member_id: str
    name: str
    member_type: Member_Type


class MemberResponse(BaseModel):
    member_id: str
    name: str
    member_type: Member_Type


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies: list[str]
