import os
import uvicorn
from app.api.routers import router
from fastapi import FastAPI

description = """
Welcome to MyVault API, your personal key to Secure Storage. 🗝️

## Personal Data Management

Safeguard your digital life with ease. From passwords to personal notes, keep everything under lock and key. 🛡️

## Passwords

Effortlessly manage your keys to the digital world:
* **Store passwords** securely.
* **Retrieve passwords** quickly when you need them.

## Secure Storage

With MyVault, your data's security is our top priority. Rest easy knowing your information is encrypted and safe. 🔒

## Users

Join the MyVault community:
* **Create user accounts** (_coming soon_).
* **Access personal vaults** and manage your data with full control.

Your data, your rules, securely stored. Welcome to MyVault. 🌟
"""


app = FastAPI(title='MyVault',
              version='1.0.0',
              description=description,
              summary = """ 
              MyVault API is your fortress for Personal Data Management and Secure Storage, especially designed for safeguarding passwords. It's built to offer an uncomplicated yet secure way to store and retrieve your most sensitive information. With encryption at its core, MyVault promises peace of mind in the digital age. From managing passwords to creating user accounts, MyVault is your reliable digital guardian. Dive into a world where your data's security and privacy come first
                """,
              contact={
                  'Hp': 'Just some guy',
                  'git': 'https://github.com/Aremis-James',
                  'email': 'devpythonaj@gmail.com'
                       })

app.include_router(router=router)


if __name__ =="__main__":
    uvicorn.run(os.getenv('UVICORN_APP')
                , host=os.getenv('UVICORN_HOST')
                , port=int(os.getenv('UVICORN_PORT'))
                , reload=True)