from typing import Union, List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "This is a contact list API"}

# contacts = {
#     0: Contact(id=0, first_name="Jean", last_name="Bonneau", phone_number="0612345678", email="jean@gmail.com"),
#     1: Contact(id=1, first_name="Guy", last_name="Tarre", phone_number="0612345600", email="guy.tarre@gmail.com"),
#     2: Contact(id=1, first_name="Gordon", last_name="Zola", phone_number="0606060606", email="g.zola@msn.com"),
# }

# GROUP ROUTES

# Get all groups
@app.get("/api/v1/groups", response_model=List[schemas.Group])
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups


# Get a group by id
@app.get("/api/v1/groups/{group_id}", response_model=schemas.Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail=f"Group with {group_id=} does not exist")
    return db_group


# Create a group
@app.post("/api/v1/groups", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.create_group(db, group)
    return db_group


# Update a group
@app.put("/api/v1/groups/{group_id}", response_model=schemas.Group)
def update_group(group_id: int, group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail=f"Group with {group_id=} does not exist")

    db_group = crud.update_group(db, group_id, group)
    return db_group


# Delete a group
@app.delete("/api/v1/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):    
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail=f"Group with {group_id=} does not exist")
    
    db_group = crud.delete_group(db, group_id)
    return {"deleted": db_group}


# CONTACT ROUTES

# Get all contacts
@app.get("/api/v1/contacts", response_model=List[schemas.Contact])
def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts


# Get a contact by id
@app.get("/api/v1/contacts/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail=f"Contact with {contact_id=} does not exist")
    return db_contact


# Get a contact by parameters


# Create a contact
@app.post("/api/v1/contacts", response_model=schemas.ContactCreate)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.create_contact(db, contact)
    return db_contact


# Update a contact
@app.patch("/api/v1/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactBase, db: Session = Depends(get_db)):
    """
    To partially update contact information, fill only the desired fields.
    """
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail=f"Contact with {contact_id=} does not exist")
    
    db_contact = crud.update_contact(db, contact_id, contact)
    
    return db_contact


# Delete a contact
@app.delete("/api/v1/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):    
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail=f"Contact with {contact_id=} does not exist")
    
    db_contact = crud.delete_contact(db, contact_id)
    return {"deleted": db_contact}