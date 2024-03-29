from passlib.hash import pbkdf2_sha256
import model, schemas
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()



def get_user_by_email(db:Session, email:schemas.UserBase):
    return db.query(model.User).filter(model.User.email == email).first()


def create_user(db:Session, user: schemas.UserCreate):
    exist = get_user_by_email(db, user.email)

    if exist:
        print(f"User with email {user.email} already exists.")

        return 
            
    db_user = model.User(email=user.email, password=pbkdf2_sha256.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



if __name__ =='__main__':
    from connection import session
    pass





