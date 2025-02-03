# Number Classification API

## Overview
This API classifies a given number and provides interesting mathematical properties.

## Endpoint
`GET /api/classify-number?number={number}`

## Features
- Determines if number is prime
- Checks for perfect number status
- Identifies Armstrong numbers
- Calculates digit sum
- Provides a fun mathematical fact

## Response Examples

### Successful Response
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is a narcissistic number."
}
```

### Error Response
```json
{
    "number": "alphabet",
    "error": true
}
```

## Local Setup
1. Clone repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `uvicorn main:app --reload`

## Deployment
Deployed on Render.com with:
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Technology Stack
- Python
- FastAPI
- Requests library
