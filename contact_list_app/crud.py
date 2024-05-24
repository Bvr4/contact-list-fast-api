from sqlalchemy.orm import Session

from . import models, schemas


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name = contact.first_name,
        last_name = contact.last_name,
        phone_number = contact.phone_number,
        email = contact.email,
        group_id = contact.group_id,
        )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db.query(models.Contact).filter(models.Contact.id == contact_id).delete()
    db.commit()
    return True


def update_contact(db: Session, contact_id, contact: schemas.ContactBase):
    # get the existing data
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).one_or_none()
    if db_contact is None:
        return None
    
    # Update model class variable from requested fields 
    for var, value in vars(contact).items():
        setattr(db_contact, var, value) if value else None

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
    

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()    


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update_group(db: Session, group_id: int, group: schemas.GroupCreate):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).one_or_none()
    if db_group is None:
        return None
    
    db_group.name = group.name
    db.add(db_group) 
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int):
    db.query(models.Group).filter(models.Group.id == group_id).delete()
    db.commit()
    return True