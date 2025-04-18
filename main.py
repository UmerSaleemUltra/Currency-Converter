import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ConvertRequest(BaseModel):
    amount: float
    currency: str

def get_conversion_rate(to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return data['rates'].get(to_currency.upper(), None)

@app.get("/")
def home():
    return {"message": "Welcome to the USD to PKR/INR Currency Converter API"}

@app.post("/convert")
def convert_currency(req: ConvertRequest):
    rate = get_conversion_rate(req.currency)
    if rate:
        converted = req.amount * rate
        return {
            "amount": req.amount,
            "converted": round(converted, 2),
            "currency": req.currency.upper(),
            "rate": rate
        }
    return {"error": "Currency not supported. Try PKR or INR"}
