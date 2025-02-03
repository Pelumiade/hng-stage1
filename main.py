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
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n <= 0:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n: int) -> bool:
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

# def get_fun_fact(number: int) -> str:
#     try:
#         response = requests.get(f"http://numbersapi.com/{number}/math")
#         return response.text if response.status_code == 200 else "No fun fact available"
#     except:
#         return "Unable to fetch fun fact"

def get_fun_fact(number: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math")
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
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("even" if number % 2 == 0 else "odd")

        
        # Construct response
        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(digit) for digit in str(number)),
            "fun_fact": get_fun_fact(number)
        }
    except ValueError:
        # Handle non-integer inputs
        raise HTTPException(status_code=400, detail={
            "number": str(number),
            "error": True,
            "message": "Invalid number input"
        })
    
   
