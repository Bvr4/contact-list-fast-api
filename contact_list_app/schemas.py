from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    group_id: Optional[int]


class ContactCreate(ContactBase):
    first_name: str
    last_name: Union[str, None] = None
    phone_number: str
    email: Union[EmailStr, None] = None
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
