import random
from datetime import datetime, timedelta
import pandas as pd

def generate_orders(n):
    orders = []
    base_time = datetime.now()
    for i in range(n):
        order = {
            "order_id": f"O{i+1}",
            "timestamp": (base_time + timedelta(seconds=i)).isoformat(),
            "symbol": "XYZ",
            "side": random.choice(["buy", "sell"]),
            "price": round(random.uniform(100, 200), 2),
            "quantity": random.randint(10, 1000),
            "trader_id": f"T{random.randint(1, 5)}"
        }
        orders.append(order)
    return orders

def generate_trades(n):
    trades = []
    base_time = datetime.now()
    for i in range(n):
        trade = {
            "trade_id": f"T{i+1}",
            "timestamp": (base_time + timedelta(seconds=i)).isoformat(),
            "symbol": "XYZ",
            "price": round(random.uniform(100, 200), 2),
            "quantity": random.randint(10, 1000),
            "buyer_id": f"B{random.randint(1, 5)}",
            "seller_id": f"S{random.randint(1, 5)}"
        }
        trades.append(trade)
    return trades

def generate_market_depth():
    depth = []
    for i in range(5):
        depth.append({
            "symbol": "XYZ",
            "bid_price": round(100 + i, 2),
            "bid_quantity": random.randint(100, 1000),
            "ask_price": round(105 + i, 2),
            "ask_quantity": random.randint(100, 1000),
            "timestamp": datetime.now().isoformat()
        })
    return depth

def generate_orders_from_uploaded_data(df: pd.DataFrame, num_orders: int, intensity: float) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    synthetic_orders = []
    base_time = datetime.now()

    for _ in range(num_orders):
        template = df.sample(1).iloc[0].to_dict()
        order = template.copy()

        if 'price' in order:
            order['price'] = round(float(order['price']) * (1 + random.uniform(-0.01, 0.01) * intensity), 2)
        if 'quantity' in order:
            order['quantity'] = int(float(order['quantity']) * (1 + random.uniform(-0.1, 0.1) * intensity))
        if 'timestamp' in order:
            order['timestamp'] = (base_time + timedelta(seconds=random.randint(0, 60))).isoformat()

        synthetic_orders.append(order)

    return pd.DataFrame(synthetic_orders)
