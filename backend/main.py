import os
import uvicorn
from app.api.routers import router
from fastapi import FastAPI



app = FastAPI()

app.include_router(router=router, prefix='/v1')


if __name__ =="__main__":
    uvicorn.run(os.getenv('UVICORN_APP')
                , host=os.getenv('UVICORN_HOST')
                , port=int(os.getenv('UVICORN_PORT'))
                , reload=True)