import time
import requests
from coin_api.get_price import GetPriceAPI
from requests.auth import HTTPBasicAuth

# API credentials - EDIT THESE
API_KEY = ""
API_SECRET = ""

# EDIT THESE
MARKET = "P2P-USDT" # TradeOgre Market
INTERVAL = 600      # Time to cancel/resumbit orders on the book
ADJ1 = 1.07         # Spread1
ADJ2 = 1.09         # Spread2

auth = HTTPBasicAuth(API_KEY, API_SECRET)

def get_coinstats_price():
    priceAPI = GetPriceAPI()
    data = priceAPI.get_usd("dvpn")
    return float(data["price"])

def get_tradeogre_balance():
    url = "https://tradeogre.com/api/v1/account/balance"
    payload = {"currency" : "P2P"}
    response = requests.post(url, auth=auth, data=payload)
    data = response.json()
    return float(data.get("balance", 0))

def get_open_orders():
    url = "https://tradeogre.com/api/v1/account/orders"
    response = requests.post(url, auth=auth)
    return response.json()

def cancel_order(uuid):
    url = "https://tradeogre.com/api/v1/order/cancel"
    payload = {"uuid": uuid}
    response = requests.post(url, auth=auth, data=payload)
    return response.json()

def cancel_open_p2p_orders():
    orders = get_open_orders()
    print(orders)
    for o in orders:
        uuid = o.get('uuid')
        if o.get("market") == MARKET:
            result = cancel_order(uuid)
            print(f"Cancelled order {uuid}: {result}")

def place_sell_order(price, amount):
    url = "https://tradeogre.com/api/v1/order/sell"
    payload = {
        "market": MARKET,
        "quantity": str(amount),
        "price": str(price)
    }
    response = requests.post(url, auth=auth, data=payload)
    return response.json()

def run_cycle():
    try:
        print("Getting P2P price from CoinStats...")
        base_price = get_coinstats_price()
        target_price1 = round(base_price * ADJ1, 8)
        target_price2 = round(base_price * ADJ2, 8)
        print(f"Target price: {target_price1} USDT")
        print(f"Target price: {target_price2} USDT")

        print("Cancelling open P2P orders...")
        cancel_open_p2p_orders()

        print("Fetching P2P balance...")
        balance = get_tradeogre_balance()
        print(f"Available balance: {balance} P2P")
        hbalance = int(balance/2)
        if balance > 0:
            print("Placing new sell order...")
            result1 = place_sell_order(target_price1, hbalance)
            result2 = place_sell_order(target_price2, hbalance)
            print("Order result:", result1)
            print("Order result:", result2)
        else:
            print("No P2P balance available to sell.")

    except Exception as e:
        print("Error during cycle:", e)

def main():
    while True:
        print("\n=== New Cycle ===")
        run_cycle()
        print(f"Waiting {INTERVAL // 60} minutes...\n")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
