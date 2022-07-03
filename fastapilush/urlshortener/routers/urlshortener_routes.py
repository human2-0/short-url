from fastapi import APIRouter, status, Request, Response
from fastapi.responses import RedirectResponse

from urlshortener import utils
from urlshortener.models import TortoiseUrl
from urlshortener.schemas import (UrlIn, UrlOut)

router = APIRouter()


@router.get("/")
async def index():
    return {"url": "shortener"}


@router.post('/url/')
async def make_url(url: UrlIn, request: Request, response: Response) -> UrlOut:
    try:
        createurl = url.dict()
        createurl['path'] = utils.create_shorturl()
        createurl['shorturl'] = request.url_for('index') + createurl.get('path')
        target = await TortoiseUrl.create(**createurl)
        target = UrlOut.from_orm(target)
        response.status_code=status.HTTP_201_CREATED
    except:
        target = await TortoiseUrl.get(**url.dict())
        target = UrlOut.from_orm(target)
        response.status_code=status.HTTP_200_OK
    return target


@router.get('/{shorturl}', status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def url_flow(shorturl: str):
    urlflow = await TortoiseUrl.get(path=shorturl)
    if urlflow:
        return RedirectResponse(urlflow.longurl, status_code=status.HTTP_308_PERMANENT_REDIRECT)
    else:
        return urlflow
