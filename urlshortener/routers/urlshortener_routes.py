from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from fastapilush.urlshortener import models, crud, utils, schemas
from fastapilush.urlshortener.database import SessionLocal, engine

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def index():
    return {"url": "shortener"}


@router.post('/url/', response_model=schemas.UrlOut)
async def make_url(url: schemas.UrlIn, response: Response, db: Session = Depends(get_db)):
    db_url = crud.get_url(db, longurl=url.longurl)

    if db_url:
        raise HTTPException(
            status_code=200,
            detail="The url already registered. Previously created short url: " + db_url.shorturl
        )
    else:
        response.status_code = status.HTTP_201_CREATED

    schemas.UrlOut.shorturl = utils.create_shorturl()
    output = {'longurl': url.longurl, 'shorturl': schemas.UrlOut.shorturl}
    targeturl = crud.create_url(db=db, url=output)
    return targeturl


@router.get("/{shorturl}")
async def shorturlflow(shorturl: str, db: Session = Depends(get_db)):
    flow = crud.get_shorturlflow(db=db, shorturl=shorturl)
    if flow is not None:
        return RedirectResponse(flow.longurl, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        raise HTTPException(status_code=400, detail="The path does not exist.")
