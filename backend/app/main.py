import os
import crud
import uvicorn
import schemas
import dependencies
from typing import Annotated
from datetime import timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, Path, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm




app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/users/login/token')

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db = Depends(dependencies.get_session)):
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
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post('/v1/users/signup/', 
          response_model= schemas.User, 
          summary='Create a new user' ,
          status_code=status.HTTP_201_CREATED, 
          tags=['sign up'])
def signup( user: schemas.UserCreate, 
        db:Session = Depends(dependencies.get_session)):
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

    return  crud.post_user(db=db, user=user)
            

@app.post('/v1/users/login/token',
          summary='Authenticate a user', 
          status_code=status.HTTP_202_ACCEPTED, 
          tags=['authentication'])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          db:Session = Depends(dependencies.get_session),
        ):
    """
    Authenticate a user and return an access token.

    Validates the user's credentials against the stored records. If successful, it issues a JWT access token
    that can be used to authenticate subsequent requests. Returns an error for incorrect username or password.

    - **form_data**: `OAuth2PasswordRequestForm` - The form data containing the username and password.
    - **db**: `Session` - The database session used to verify the user's credentials.
    
    **Response**:
    - Returns a dictionary with the user's access token and the token type if authentication is successful.
    
    Raises HTTP 401 for incorrect username or password.
    """

    user = crud.get_user_by_email(db,email=form_data.username)
    if not user or not dependencies.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=30)
    access_token = dependencies.create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    
    return schemas.Token(access_token=access_token, token_type='bearer')

@app.get('/v1/users/current_user', tags=['authentication'])
def read_current_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user

@app.post('/v1/users/current_user/items', 
          response_model= schemas.Item, 
          summary='Add a new item', 
          status_code=status.HTTP_201_CREATED, 
          tags=['item'])
def add_user_item(item: schemas.ItemCreate, 
                current_user :schemas.User = Depends(get_current_user),
                db:Session = Depends(dependencies.get_session)):
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
    return crud.post_item(db=db, item=item, user_id=current_user.id)


@app.get('/v1/users/current_user/items', 
        response_model=list[schemas.Item],
        summary='Retrieve a list of items',
        tags=['item'])
def get_user_items(skip:int=0, limit:int = 10,
                current_user: schemas.User = Depends(get_current_user),
                db:Session = Depends(dependencies.get_session)):
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
    user = crud.get_user(db=db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    items = crud.get_user_items(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return items


@app.patch('/v1/users/current_user/items/{item_id}',
          response_model= schemas.Item,
          tags=['item'],
          summary='Update an item',
          status_code=status.HTTP_202_ACCEPTED
          )
def update_item(item_id: Annotated[int, Path(gt=0)], 
                item_update: schemas.ItemUpdate,
                current_user: schemas.User = Depends(get_current_user),
                db:Session = Depends(dependencies.get_session)):
    """
    Update an item's details for the specified user.

    Parameters:
    - user_id: int - The ID of the user who owns the item.
    - item_id: int - The ID of the item to be updated.
    - item_update: schemas.ItemUpdate - A Pydantic model representing the fields to update.
    - db: Session - Dependency that provides a SQLAlchemy database session.

    Returns:
    - The updated `schemas.Item` model of the item.
    """
    item = crud.get_user_item_by_id(db=db,user_id=current_user.id, item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    

    new_data = item_update.model_dump(exclude_unset=True)
    update_item = crud.update_item(db=db, item=item, item_update=new_data)
    return update_item


if __name__ =="__main__":
    uvicorn.run(os.getenv('UVICORN_APP')
                , host=os.getenv('UVICORN_HOST')
                , port=int(os.getenv('UVICORN_PORT'))
                , reload=True)