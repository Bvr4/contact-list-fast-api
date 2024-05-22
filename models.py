from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    phone_number = Column(Integer)
    email = Column(String)
    group_id = Column(Integer, ForeignKey("group.id"))
    
    group = relationship("Group", back_populates="contacts")
    

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    contacts = relationship("Contact", back_populates="group")