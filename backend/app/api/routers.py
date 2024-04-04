import os
from app.api import crud, dependencies
from backend.app.api import schemas
from typing import Annotated
from datetime import timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, Path, status, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

router =APIRouter()

tags = schemas.Tags

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

def get_current_user(security_scopes : SecurityScopes,
                     token: Annotated[str, Depends(oauth2_scheme)], 
                     db = Depends(dependencies.get_session)):
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


@router.post('/v1/login/token',
          summary='Authenticate a user', 
          status_code=status.HTTP_202_ACCEPTED, 
          tags=[tags.auth])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          
          db:Session = Depends(dependencies.get_session),
        ):
    """
    Authenticates a user and issues a JWT access token.

    This endpoint verifies the user's credentials (username and password) against the database records.
    If the credentials are validated, it returns a JWT access token that can be used for subsequent authenticated requests.
    
    Parameters:
    - form_data: OAuth2PasswordRequestForm containing the user's username and password.
    - db: The database session.

    Returns:
    - A JSON object containing the JWT access token and its type.

    Raises HTTP 401 if the username or password is incorrect.
    """

    user = crud.get_user_by_email(db,email=form_data.username)
    if not user or not dependencies.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=30)
    access_token = dependencies.create_access_token(data={'sub': user.email, 'scopes': user.scopes}, expires_delta=access_token_expires)
    
    return schemas.Token(access_token=access_token, token_type='bearer')


@router.post('/v1/signup/', response_model= schemas.User, summary='Create a new user', status_code=status.HTTP_201_CREATED, tags=[tags.user])
def signup( user: schemas.UserCreate, 
        db:Session = Depends(dependencies.get_session)):
    """
    Registers a new user with an email and password.

    This endpoint attempts to create a new user in the database with the given email and password. 
    It checks if a user with the specified email already exists and, if so, returns a 400 error indicating the email is already registered.

    Parameters:
    - user: UserCreate schema containing the email and password of the new user.
    - db: The database session.

    Returns:
    - The newly created User schema including the user's email and a system-assigned unique ID.
    
    Raises HTTP 400 if the email is already registered.
    """

    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    return  crud.post_user(db=db, user=user)


@router.get('/v1/user', tags=[tags.user], summary='Retrieves the currently authenticated user')
def read_current_user(current_user: Annotated[schemas.User, Security(get_current_user, scopes=['user:read', 'user:write'])]):
    """
    Retrieves the currently authenticated user's information.

    This endpoint returns the details of the user who is currently authenticated via JWT token.
    
    Parameters:
    - current_user: The currently authenticated User schema obtained through JWT token authentication.

    Returns:
    - The User schema of the currently authenticated user.
    """
    return current_user


@router.post('/v1/user/items', response_model= schemas.Item, summary='Add a new item', status_code=status.HTTP_201_CREATED, tags=[tags.items])
def add_user_item(item: schemas.ItemCreate, 
                current_user :schemas.User = Depends(get_current_user),
                db:Session = Depends(dependencies.get_session)):
    """
    Adds a new item to the collection of the currently authenticated user.

    Parameters:
    - item: ItemCreate schema containing the details of the item to be added.
    - current_user: The currently authenticated User schema.
    - db: The database session.

    Returns:
    - The newly added Item schema including its details and the ID of the associated user.
    """
    return crud.post_item(db=db, item=item, user_id=current_user.id)


@router.get('/v1/user/items', response_model=list[schemas.Item], summary='Retrieve a list of items', tags=[tags.items])
def get_user_items(skip:int=0, limit:int = 10,
                current_user: schemas.User = Depends(get_current_user),
                db:Session = Depends(dependencies.get_session)):
    """
    Retrieves a paginated list of items owned by the currently authenticated user.

    Parameters:
    - skip: Number of items to skip (for pagination).
    - limit: Maximum number of items to return (for pagination).
    - current_user: The currently authenticated User schema.
    - db: The database session.

    Returns:
    - A list of Item schemas representing the items owned by the user.
    """
    user = crud.get_user(db=db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    items = crud.get_user_items(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return items


@router.patch('/v1/user/items/{item_id}', response_model= schemas.Item, tags=[tags.items], summary='Update an item', status_code=status.HTTP_202_ACCEPTED)
def update_item(item_id: Annotated[int, Path(gt=0)], 
                item_update: schemas.ItemUpdate,
                current_user: schemas.User = Depends(get_current_user),
                db:Session = Depends(dependencies.get_session)):
    """
    Updates the details of an item owned by the currently authenticated user.

    Parameters:
    - item_id: The unique identifier of the item to be updated.
    - item_update: ItemUpdate schema containing the fields to be updated.
    - current_user: The currently authenticated User schema.
    - db: The database session.

    Returns:
    - The updated Item schema.

    Raises HTTP 404 if the item is not found.
    """
    item = crud.get_user_item_by_id(db=db,user_id=current_user.id, item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    

    new_data = item_update.model_dump(exclude_unset=True)
    update_item = crud.update_item(db=db, item=item, item_update=new_data)
    return update_item