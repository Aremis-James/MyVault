import typing
from ..api import models, schemas, crud
from ..core import security, config

import os
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jose import jwt, JWTError

from fastapi import Depends, status, HTTPException
from fastapi.security import SecurityScopes


########## DataBase Dependencies ##########


engine = create_engine(config.DATABASE_URL)
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()



def get_current_user(security_scopes : SecurityScopes,
                     token: Annotated[str, Depends(security.oauth2_scheme)], 
                     db = Depends(get_session)):
    if security_scopes:
        authenticate = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate = 'Bearer'
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},    
        )
    try:
        payload =jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = schemas.TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not Enough permissions',
                headers={'WWW-Authenticate': authenticate}
            )
    return user

######## Password Auth ########        

# pwd_context = CryptContext(schemes=[os.getenv('ENCRYPT')], deprecated='auto')

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


#################### Token Auth #######################

# def create_access_token(data:dict, expires_delta: timedelta| None= None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({'exp': expire})
#     encode_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm='HS256')
#     return encode_jwt

