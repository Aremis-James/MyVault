
import tomllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import keyring
import os


def session():
    load_dotenv()
    absolut_path = f'{os.getenv("ABS_PATH")}'
    
    with open(absolut_path,'rb') as file:
        toml_load = tomllib.load(file)['db']
        user = toml_load['user']
        password = keyring.get_password(os.getenv('SYS'), os.getenv('UN'))
        hostname = toml_load['host']
        database_name = toml_load['database']

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{hostname}/{database_name}")
    Session = sessionmaker(bind=engine)

    return Session()


