import asyncio
import httpx
import pytest
import pytest_asyncio

from asgi_lifespan import LifespanManager
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)





@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url='http://127.0.0.1:8000') as test_client:
            yield test_client


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"url": "shortener"}


@pytest.mark.asyncio
async def test_url_exists(test_client: httpx.AsyncClient):
    url = {
  "longurl": "http://google.com"
}
    response = await test_client.post("/url/", json=url)
    assert response.status_code == 200
    assert response.json() == {"shorturl": "http://127.0.0.1:8000/zLm2xyvM"}


def test_invalid_url():
    response = client.post("/url/", json={"longurl": "www.google.com"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "longurl"
                ],
                "msg": "invalid or missing URL scheme",
                "type": "value_error.url.scheme"
            }
        ]
    }


@pytest.mark.asyncio
async def test_url_flow(test_client: httpx.AsyncClient):
    response = await test_client.get("/hashcash")
    assert response.status_code == 404
    assert response.json() == {"detail": "Object does not exist"}
