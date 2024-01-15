from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_log(db: Session, identifier: str):
    return db.query(models.User).filter(models.User.email == identifier).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_resource(db: Session, user_id: int, file_path: str):
    
    new_resource = models.Resource(user_id=user_id, pdf=file_path)
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource.id


def create_resource_url(db: Session, user_id: int, url: str):
    
    new_resource = models.Resource(user_id=user_id, url=url)
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource.id