from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"url": "shortener"}


def test_url_exists():
    response = client.post("/url/", json={"longurl": "http://google.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "The url already registered. Previously created short url: 5vR0lrDz"}


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


def test_url_flow():
    response = client.get("/hashcash")
    assert response.status_code == 400
    assert response.json() == {"detail": "The path does not exist."}
