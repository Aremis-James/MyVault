import tomllib, keyring, os
from dotenv import load_dotenv



load_dotenv()
absolut_path = f'{os.getenv("ABS_PATH")}'
def __config_engine():
    with open(absolut_path,'rb') as file:
        toml_load = tomllib.load(file)['db']
        user = toml_load['user']
        password = keyring.get_password(os.getenv('SYSTEM'), os.getenv('UN'))
        hostname = toml_load['host']
        database_name = toml_load['database']
    database_url = f"postgresql+psycopg2://{user}:{password}@{hostname}/{database_name}"
    return database_url

DATABASE_URL = __config_engine()
