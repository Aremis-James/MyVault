from passlib.hash import pbkdf2_sha256
from .model import User
from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError



class UserOperations:
    def __init__(self, session: Session) -> None:
        self.__session = session


    def get_user(self, by: Literal['email', 'id'], value:str):
        try:
            if by == 'email' and value.isdigit():
                raise ValueError("Name should not be numeric.")
            
            if by =='id' and value.isalpha():
                raise ValueError("Id should not contain letters.")
            
            match by:
                case 'email':
                    query = select(User).where(User.email == value)

                case 'id':
                    query = select(User).where(User.id == int(value))

                case _ :
                    raise ValueError("Invalid search criterion")
                
            result = self.__session.execute(query).scalars().first()
            return result
                

        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

            
    def add_user(self, email:str, password:str):
        try:
            exist = self.__session.query(User).filter_by(email=email).first()
            if exist:
                print(f"User with email {email} already exists.")
                return 
            
            hash_password = pbkdf2_sha256.hash(password)
            new_user = User(email=email, password=hash_password)

            self.__session.add(new_user)
            self.__session.commit()

        except IntegrityError:
            print(f"Failed to add user {email}: email must be unique.")
            self.__session.rollback()
        except Exception as e:
            self.__session.rollback()
            raise e
        finally:
            self.__session.close()


    def update_user(self):
        pass

    def delete_user(self, user_id:User.id):
        try:
            set_for_deletion = select(User).where(User.id==user_id)
            results = self.__session.execute(set_for_deletion).scalar()
            self.__session.delete(results)
            self.__session.commit()
            print('User deleted')
        except Exception as e:
            print(f'{e}')
        finally:
            self.__session.close()



class PasswordOperations:
    def __init__(self, session:Session):
        self.__session = session
        pass

    def add_password(self):
        pass

    def get_password(self):
        pass

    def update_password(self):
        pass

    def remove_password(self):
        pass


