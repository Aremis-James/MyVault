from backend.app.api import models
from backend.app.api import schemas
from app.api import dependencies
from sqlalchemy.orm import Session

###################### User Crud ##############################
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()



def get_user_by_email(db:Session, email:schemas.UserBase):
    return db.query(models.User).filter(models.User.email == email).first()


def post_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=dependencies.hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session, user: models.User, user_update:dict):
    for key, value in user_update.items():
        if hasattr(user,key):
            setattr(user, key,value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user





###################### Item Crud ##############################

def get_user_item_by_id(db:Session, user_id:int, item_id: int):
    return db.query(models.Item).filter(models.Item.user_id == user_id, models.Item.id == item_id).first()


def get_user_items(db:Session, user_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.user_id==user_id).offset(skip).limit(limit).all()


def post_item(db:Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db:Session, item: models.Item, item_update: dict):

    for key, value in  item_update.items():
        if hasattr(item, key):
            setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

if __name__ =='__main__':
    pass






