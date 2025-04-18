import requests

def get_conversion_rate(to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()

    return data['rates'].get(to_currency, None)

def convert_currency(amount, currency):
    rate = get_conversion_rate(currency)
    if rate:
        converted = amount * rate
        print(f"{amount} USD = {converted:.2f} {currency}")
    else:
        print("Currency not supported.")

# Input
try:
    amount = float(input("Enter amount in USD: "))
    currency = input("Convert to (PKR or INR): ").upper()
    convert_currency(amount, currency)
except ValueError:
    print("Invalid amount.")
