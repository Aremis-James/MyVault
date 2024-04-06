import os
from jose import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime , timezone


load_dotenv()
pwd_context = CryptContext(schemes=[os.getenv('ENCRYPT')], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/login/token',
                                     scopes={
                                            'user:read': 'Allows reading user data',
                                            'user:write': 'Allows writing user data',
                                            'user:delete': 'Allows deleting user data',
                                            'admin:read': 'Allows reading all data',
                                            'admin:write': 'Allows writing all data',
                                            'admin:delete': 'Allows deleting all data',
                                            }
)

def create_access_token(data:dict, expires_delta: timedelta| None= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm='HS256')
    return encode_jwt
if __name__ == "__main__":
    print(os.getenv('ENCRYPT'))