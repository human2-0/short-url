from sqlalchemy import Column, Integer, String

from fastapilush.urlshortener.database import Base


class UrlShortener(Base):
    __tablename__ = "shorturl"

    id = Column(Integer, primary_key=True, index=True)
    longurl = Column(String, unique=True, index=True)
    shorturl = Column(String, unique=True, index=True)
