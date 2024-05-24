from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    contacts = relationship("Contact", back_populates="group")


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    
    group = relationship("Group", back_populates="contacts")
    