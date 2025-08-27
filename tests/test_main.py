from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance for your FastAPI app
client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint to ensure it returns the correct welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_add_numbers_success():
    """
    Test the add endpoint with valid numerical inputs.
    """
    response = client.post("/add", json={"a": 5, "b": 10})
    assert response.status_code == 200
    assert response.json() == {"result": 15.0}

def test_add_numbers_with_floats():
    """
    Test the add endpoint with floating-point numbers.
    """
    response = client.post("/add", json={"a": 2.5, "b": 3.5})
    assert response.status_code == 200
    assert response.json() == {"result": 6.0}

def test_add_numbers_with_negative_numbers():
    """
    Test the add endpoint with negative numbers.
    """
    response = client.post("/add", json={"a": -5, "b": -10})
    assert response.status_code == 200
    assert response.json() == {"result": -15.0}

def test_add_numbers_with_invalid_input():
    """
    Test the add endpoint with invalid string input to ensure it fails.
    FastAPI's Pydantic validation handles this automatically, resulting in a 422 error.
    """
    response = client.post("/add", json={"a": "invalid", "b": 10})
    assert response.status_code == 422