from sqlalchemy import Column, Integer, String
from database import Base


class UrlShortener(Base):
    __tablename__ = "urlshortener"

    id = Column(Integer, primary_key=True, index=True)
    longurl = Column(String, unique=True, index=True)
    shorturl = Column(String, unique=True, index=True)
