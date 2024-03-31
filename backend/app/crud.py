import models, schemas, dependencies
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()



def get_user_by_email(db:Session, email:schemas.UserBase):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=dependencies.hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_user_items(db:Session, user_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.user_id==user_id).offset(skip).limit(limit).all()


def create_item(db:Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

if __name__ =='__main__':
    pass






