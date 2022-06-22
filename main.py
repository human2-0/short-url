from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas
import utils


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index():
    return {"url": "shortener"}


@app.post('/url/', response_model=schemas.UrlOut)
def make_url(url: schemas.UrlIn, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_url(db, longurl=url.longurl)
    if db_url:
        raise HTTPException(
            status_code=400,
            detail="The url already registered. Previously created short url: " + db_url.shorturl
        )
    schemas.UrlOut.shorturl = utils.create_shorturl()
    output = {'longurl': url.longurl, 'shorturl': schemas.UrlOut.shorturl}
    targeturl = crud.create_url(db=db, url=output)
    return targeturl


@app.get("/{shorturl}")
def shorturlflow(shorturl: str, db: Session = Depends(get_db)):
    flow = crud.get_shorturlflow(db=db, shorturl=shorturl)
    if flow is not None:
        return RedirectResponse(flow.longurl)
    else:
        raise HTTPException(status_code=400, detail="The path does not exist.")
