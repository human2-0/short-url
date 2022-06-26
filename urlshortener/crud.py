from sqlalchemy.orm import Session

from fastapilush.urlshortener import models


def get_url(db: Session, longurl: str):
    return db.query(models.UrlShortener).filter(models.UrlShortener.longurl == longurl).first()


def get_shorturlflow(db: Session, shorturl: str):
    return db.query(models.UrlShortener).filter(models.UrlShortener.shorturl == shorturl).first()


def create_url(db: Session, url):
    db_url = models.UrlShortener(**url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
