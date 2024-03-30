from typing import Union
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException
from dependencies import get_session
from crud import get_user_by_email
import schemas 
import uvicorn


app = FastAPI()

def verify_password(plain_text:str , hashed:str):
    pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
    return pwd_context.verify(plain_text, hashed)


@app.post('/user/login')
def login(user_login: schemas.UserCreate, db:Session = Depends(get_session)):
    user = get_user_by_email(db, user_login.email)
    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"id": user.id}

@app.get('user/items')
def get_items():
    pass




















if __name__ =='__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)