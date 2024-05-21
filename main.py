from typing import Union
from fastapi import FastAPI, HTTPException
from models import Contact

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is a contact list API"}

contacts = {
    0: Contact(id=0, first_name="Jean", last_name="Bonneau", phone_number="0612345678", email="jean@gmail.com"),
    1: Contact(id=1, first_name="Guy", last_name="Tarre", phone_number="0612345600", email="guy.tarre@gmail.com"),
    2: Contact(id=1, first_name="Gordon", last_name="Zola", phone_number="0606060606", email="g.zola@msn.com"),
}

# Get all contacts
@app.get("/api/v1/contacts")
async def get_contacts():
    return {"contacts": contacts}

# Get a contact by id
@app.get("/api/v1/contacts/{contact_id}")
async def get_contact(contact_id: int):
    if contact_id not in contacts:
        HTTPException(status_code=404, detail=f"Contact with {contact_id=} does not exist.")

    return contacts[contact_id]

# Get a contact by parameters

# Create a contact
@app.post("/api/v1/contacts")
async def create_contact(contact: Contact):
    if contact.id in contacts:
        HTTPException(status_code=400, detail=f"Contact with {contact.id=} already exist.")
    contacts[contact.id] = contact
    return {"added": contact}

# Update a contact
@app.put("/api/v1/contacts/{contact_id}")
async def update_contact(
    contact_id: int, 
    first_name: Union[str, None] = None,
    last_name: Union[str, None] = None,
    phone_number: Union[int, None] = None,
    email: Union[str, None] = None
    ):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail=f"Contact with {contact_id=} does not exist.")
    
    contact = contacts[contact_id]
    # update if the fiels is present
    if first_name:
        contact.first_name = first_name
    if last_name:
        contact.last_name = last_name
    if phone_number:
        contact.phone_number = phone_number
    if email:
        contact.email = email

    contacts[contact_id] = contact

    return {"updated": contact}

# Delete a contact
@app.delete("/api/v1/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail=f"Contact with {contact_id=} does not exist.")

    contact = contacts.pop(contact_id)
    return {"deleted": contact}