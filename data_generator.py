import random
from datetime import datetime, timedelta
import pandas as pd

def generate_orders(n):
    base_time = datetime.now()
    return [{
        "order_id": f"O{i+1}",
        "timestamp": (base_time + timedelta(seconds=i)).isoformat(),
        "symbol": "XYZ",
        "side": random.choice(["buy", "sell"]),
        "price": round(random.uniform(100, 200), 2),
        "quantity": random.randint(10, 1000),
        "trader_id": f"T{random.randint(1, 5)}"
    } for i in range(n)]

def generate_trades(n):
    base_time = datetime.now()
    return [{
        "trade_id": f"T{i+1}",
        "timestamp": (base_time + timedelta(seconds=i)).isoformat(),
        "symbol": "XYZ",
        "price": round(random.uniform(100, 200), 2),
        "quantity": random.randint(10, 1000),
        "buyer_id": f"B{random.randint(1, 5)}",
        "seller_id": f"S{random.randint(1, 5)}"
    } for i in range(n)]

def generate_market_depth():
    return [{
        "symbol": "XYZ",
        "bid_price": round(100 + i, 2),
        "bid_quantity": random.randint(100, 1000),
        "ask_price": round(105 + i, 2),
        "ask_quantity": random.randint(100, 1000),
        "timestamp": datetime.now().isoformat()
    } for i in range(5)]

def generate_orders_from_uploaded_data(df, num_orders):
    return df.sample(n=num_orders, replace=True).reset_index(drop=True)

def generate_trades_from_uploaded_data(df, num_trades):
    return df.sample(n=num_trades, replace=True).reset_index(drop=True)

def generate_market_depth_from_uploaded_data(df):
    return df.sample(n=len(df), replace=True).reset_index(drop=True)
