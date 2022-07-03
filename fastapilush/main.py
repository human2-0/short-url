import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from urlshortener.routers.urlshortener_routes import router

app = FastAPI()
app.include_router(router, prefix='', tags=['urlshortener'])



TORTOISE_ORM = {
    "connections": {"default": "sqlite://sql_app.db"},
    "apps": {
        "models": {
            "models": ["urlshortener.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app='main:app')
