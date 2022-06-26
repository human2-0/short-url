import uvicorn
from fastapi import FastAPI

from fastapilush.urlshortener.routers.urlshortener_routes import router

app = FastAPI()

app.include_router(router, prefix='', tags=['urlshortener'])

if __name__ == "__main__":
    uvicorn.run(app='main:app')
