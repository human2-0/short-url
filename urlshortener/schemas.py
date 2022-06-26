from pydantic import BaseModel, AnyUrl


class UrlIn(BaseModel):
    longurl: AnyUrl


class UrlOut(BaseModel):
    shorturl: str | None = None

    class Config:
        orm_mode = True
