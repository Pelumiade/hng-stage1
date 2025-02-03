import math
import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    # Primes are positive integers greater than 1
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(abs(n))) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    # Perfect numbers are positive integers
    if n <= 0:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n: int) -> bool:
    # Armstrong check works for positive integers
    if n < 0:
        return False
    num_str = str(abs(n))
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == abs(n)

def get_fun_fact(number: int) -> str:
    # Using abs to handle negative numbers for fact retrieval
    try:
        response = requests.get(f"http://numbersapi.com/{abs(number)}/math")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return "Unable to fetch fun fact"

@app.get("/api/classify-number")
async def classify_number(number: Union[int, str] = Query(None)):
    if number is None:
        raise HTTPException(status_code=400, detail={
            "number": None,
            "error": True,
            "message": "Number parameter is required"
        })

    try:
        # Convert to integer
        number = int(number)

        # Determine number properties
        properties: List[str] = []
        
        # Armstrong check
        if is_armstrong(number):
            properties.append("armstrong")
        
        # Parity check
        properties.append("even" if number % 2 == 0 else "odd")

        # Construct response
        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(digit) for digit in str(abs(number))),
            "fun_fact": get_fun_fact(number)
        }
    except ValueError:
        # Handle non-integer inputs
        raise HTTPException(status_code=400, detail={
            "number": str(number),
            "error": True,
            "message": "Invalid number input"
        })
    