from typing import Union
from fastapi import FastAPI, HTTPException, logger
from database.connection import session


app = FastAPI()

#Dependency
def get_session():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

