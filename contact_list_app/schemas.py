from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    group_id: Optional[int] = None


class ContactCreate(ContactBase):
    first_name: str
    phone_number: str
    group_id: int


class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True



class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    contacts: List[Contact] = []

    class Config:
        orm_mode = True
