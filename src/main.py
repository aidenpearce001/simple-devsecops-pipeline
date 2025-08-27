# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create a FastAPI instance
app = FastAPI()

class CalculationRequest(BaseModel):
    """
    Pydantic model for the request body.
    """
    a: float
    b: float

@app.get("/")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/add")
def add_numbers(request: CalculationRequest):
    """
    Adds two numbers provided in the request body.

    Args:
        request: A Pydantic model containing two numbers 'a' and 'b'.

    Returns:
        A dictionary with the result of the addition.
    """
    # Simple input validation
    if not isinstance(request.a, (int, float)) or not isinstance(request.b, (int, float)):
        raise HTTPException(status_code=400, detail="Inputs must be numbers.")
    
    result = request.a + request.b
    
    return {"result": result}