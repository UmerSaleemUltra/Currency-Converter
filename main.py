import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Currency Converter</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f3f4f6;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 300px;
            }

            h1 {
                color: #4CAF50;
                margin-bottom: 20px;
                font-size: 24px;
            }

            input[type="number"], input[type="text"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
                border: 1px solid #ccc;
                font-size: 16px;
            }

            button {
                width: 100%;
                padding: 12px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #45a049;
            }

            #result {
                margin-top: 20px;
                font-size: 18px;
                color: #333;
                font-weight: bold;
            }

            .error {
                color: red;
            }
        </style>
        <script>
        async function convertCurrency() {
            let amount = parseFloat(document.getElementById("amount").value);
            let currency = document.getElementById("currency").value.toUpperCase();
            const response = await fetch("/convert", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ amount, currency })
            });
            const data = await response.json();
            if (data.converted) {
                document.getElementById("result").innerHTML = `${amount} USD = ${data.converted} ${currency}`;
                document.getElementById("result").classList.remove("error");
            } else {
                document.getElementById("result").innerHTML = "Error: " + data.error;
                document.getElementById("result").classList.add("error");
            }
        }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Currency Converter</h1>
            <input type="number" id="amount" placeholder="Enter amount in USD">
            <input type="text" id="currency" placeholder="Convert to (PKR or INR)">
            <button onclick="convertCurrency()">Convert</button>
            <div id="result"></div>
        </div>
    </body>
    </html>
    """

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
