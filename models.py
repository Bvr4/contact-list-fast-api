from fastapi import FastAPI
from pydantic import BaseModel


class Contact(BaseModel):
    """Representation of a contact in the system."""
    
    id: int
    first_name: str
    last_name: str
    phone_number: int
    email: str