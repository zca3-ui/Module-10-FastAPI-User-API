
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint, a, b, expected",
    [
        ("/add", 10, 5, 15),
        ("/subtract", 10, 5, 5),
        ("/multiply", 10, 5, 50),
        ("/divide", 10, 5, 2),
    ],
)
def test_calculator_operations(client, endpoint, a, b, expected):
    response = client.post(
        endpoint,
        json={"a": a, "b": b}
    )

    assert response.status_code == 200
    assert response.json()["result"] == expected


def test_divide_by_zero(client):
    response = client.post(
        "/divide",
        json={"a": 10, "b": 0}
    )

    assert response.status_code == 400
    assert "Cannot divide by zero!" in response.json()["error"]


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Hello World" in response.text
