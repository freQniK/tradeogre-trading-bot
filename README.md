# tradeogre-trading-bot

A basic cancel and sell order book bot for TradeOgre. It takes the balance of p2p and splits it in half and creates sell orders for the desired price times spread1/2.



# Install

clone the repo and edit the following files

```shell
p2ptradingbot.py
```

And edit the following fields at the top of the script:

```python
# API credentials - EDIT THESE
API_KEY = ""
API_SECRET = ""

# EDIT THESE
MARKET = "P2P-USDT" # TradeOgre Market
INTERVAL = 600      # Time to cancel/resumbit sell orders on the book
ADJ1 = 1.07         # Spread1
ADJ2 = 1.09         # Spread2
```

Also, edit the following files with your CoinStats.app API keys. Which can be had at https://coinstats.app

```shell
coin_api/scrtxxs.py
```

Edit the following fields:

```python
COINSTATS_API_KEYS = ["API KEY", "API KEY 2" ]   

```

You only need one API KEY, but it should be enclosed in `[]`

Then run:

```shell
python3 p2ptradingbot.py
```
