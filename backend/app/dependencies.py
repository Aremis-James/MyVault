from datetime import timedelta, datetime , timezone
import tomllib, models, keyring, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

########## DataBase Dependencies ##########

load_dotenv()
absolut_path = f'{os.getenv("ABS_PATH")}'

with open(absolut_path,'rb') as file:
    toml_load = tomllib.load(file)['db']
    user = toml_load['user']
    password = keyring.get_password(os.getenv('SYSTEM'), os.getenv('UN'))
    hostname = toml_load['host']
    database_name = toml_load['database']

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{hostname}/{database_name}")
models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


######## Password Auth ########        

pwd_context = CryptContext(schemes=[os.getenv('ENCRYPT')], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#################### Token Auth #######################
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_access_token(data:dict, expires_delta: timedelta| None= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm='HS256')
    return encode_jwt


