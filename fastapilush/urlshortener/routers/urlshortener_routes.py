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
async def make_url(url: UrlIn ,request: Request, response: Response) -> UrlOut:
    try:
        createurl = url.dict()
        # the called function create_shorturl is trying to create a unique path for the long url
        # it is safe from a potential collision of short path code doubled in a db.
        createurl['path'] = await utils.create_shorturl()
        createurl['shorturl'] = request.url_for('index') + createurl.get('path')
        # let's try to create a short url using provided data.
        # Database model "TortoiseUrl" requires a unique long url.
        # If the url to shorten exists in the database it will raise an error, taking us to except block.
        # Otherwise, we can continue and finally return shorten url.
        #
        #
        target = await TortoiseUrl.create(**createurl)
        response.status_code = status.HTTP_201_CREATED
    except:
        # Landing to this block, means retrieving already existing long url and serving it to the client.
        target = await TortoiseUrl.get(**url.dict())
        response.status_code = status.HTTP_200_OK
    target = UrlOut.from_orm(target)
    return target


@router.get('/{shorturl}', status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def url_flow(shorturl: str):
    urlflow = await TortoiseUrl.get(path=shorturl)
    if urlflow:
        return RedirectResponse(urlflow.longurl, status_code=status.HTTP_308_PERMANENT_REDIRECT)
