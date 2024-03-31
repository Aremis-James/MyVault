from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Path, status, HTTPException
from typing import Annotated
import crud
import schemas
import dependencies
import uvicorn
import os



app = FastAPI()


@app.get("/", tags=['home'])
def home():
    return {"message": "Hello World"}


@app.post('/v1/users/signup', 
          response_model= schemas.User, 
          summary='Create a new user' ,
          status_code=status.HTTP_201_CREATED, 
          tags=['user'])

def signup( user: schemas.UserCreate, db:Session = Depends(dependencies.get_session)):
    """
    Create a new user with the provided email and password.

    This endpoint will attempt to create a new user in the database with the information provided in the `user` object. 
    If a user with the given email already exists, it will respond with a 400 error indicating that the email is already registered.

    Parameters:
    - user: schemas.UserCreate - a Pydantic model representing the user to be created, including email and password.
    - db: Session - Dependency that provides a SQLAlchemy database session from `dependencies.get_session`.

    Returns:
    - A `schemas.User` model of the newly created user, including their email and an automatically assigned id.
    """

    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    return  crud.create_user(db=db, user=user)
            

@app.post('/v1/users/login',
          summary='Authenticate a user', 
          status_code=status.HTTP_202_ACCEPTED, 
          tags=['user'])

def login(user_login: schemas.UserCreate, db:Session = Depends(dependencies.get_session)):
    """
    Authenticate a user based on email and password.

    This endpoint verifies the provided credentials against the stored records. If the credentials are correct, 
    it returns the user's ID. Otherwise, it responds with a 400 error indicating incorrect username or password.

    Parameters:
    - user_login: schemas.UserCreate - a Pydantic model representing the user attempting to log in, 
      including email and password.
    - db: Session - Dependency that provides a SQLAlchemy database session from `dependencies.get_session`.

    Returns:
    - A dictionary with the user's `id` if authentication is successful.
    """

    user = crud.get_user_by_email(db, user_login.email)
    if not user or not dependencies.verify_password(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    return  {'id': user.id}


@app.post('/v1/users/{user_id}/items/', 
          response_model= schemas.Item, 
          summary='Add a new item', 
          status_code=status.HTTP_201_CREATED, 
          tags=['item'])

def add_user_item(user_id:Annotated [int, Path(gt=0)], item: schemas.ItemCreate, db:Session = Depends(dependencies.get_session)):
    """
    Add a new item to the specified user's collection.

    This endpoint associates a new item with the user identified by `user_id`. The item's details are provided 
    in the `item` object. The operation will fail with a 400 error if the user does not exist.

    Parameters:
    - user_id: int - The ID of the user to whom the item will be added. Must be greater than 0.
    - item: schemas.ItemCreate - A Pydantic model representing the item to be added, including its details.
    - db: Session - Dependency that provides a SQLAlchemy database session from `dependencies.get_session`.

    Returns:
    - A `schemas.Item` model of the newly added item, including its details and the ID of the associated user.
    """
    return crud.create_item(db=db, item=item, user_id=user_id)


@app.get('/v1/users/{user_id}/items', 
        response_model=list[schemas.Item],
        summary='Retrieve a list of items',
        tags=['item'])
def get_user_items(user_id: Annotated [int, Path(gt=0)],skip:int=0, limit:int = 10, db:Session = Depends(dependencies.get_session)):
    """
    Retrieve a list of items owned by the specified user.

    This endpoint returns a list of items associated with the user identified by `user_id`, 
    supporting pagination through `skip` and `limit` parameters. If the user does not exist, 
    it responds with a 400 error.

    Parameters:
    - user_id: int - The ID of the user whose items are being retrieved. Must be greater than 0.
    - skip: int - The number of items to skip (for pagination).
    - limit: int - The maximum number of items to return (for pagination).
    - db: Session - Dependency that provides a SQLAlchemy database session from `dependencies.get_session`.

    Returns:
    - A list of `schemas.Item` models representing the items owned by the user.
    """
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    items = crud.get_user_items(db=db, user_id=user_id, skip=skip, limit=limit)
    return items


# @app.get('/v1/users/items', response_model=list[schemas.Item])
# def get_items(skip:int=0, limit:int = 10, db:Session = Depends(dependencies.get_session)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items




if __name__ =="__main__":
    uvicorn.run(os.getenv('UVICORN_APP')
                , host=os.getenv('UVICORN_HOST')
                , port=int(os.getenv('UVICORN_PORT'))
                , reload=True)