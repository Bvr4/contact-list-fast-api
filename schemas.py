from typing import List, Union
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    first_name: str
    last_name: Union[str, None] = None
    phone_number: int
    email: Union[EmailStr, None] = None


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    group_id: int

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