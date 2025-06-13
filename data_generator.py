import pandas as pd
import numpy as np
import random

def simulate_data(order_count=10, trade_count=10, orders_df=None, trades_df=None, market_depth_df=None):
    # Helper function to generate a single alert-triggering order
    def generate_order(i):
        return {
            "OrderID": f"O{i+1}",
            "Trader": f"Trader_{random.randint(1, 5)}",
            "Instrument": "XYZ",
            "Price": round(random.uniform(101, 150), 2),
            "BaseCcyQty": random.randint(51, 100),
            "Side": random.choice(["Buy", "Sell"]),
            "simulated": True
        }

    # Helper function to generate a single alert-triggering trade
    def generate_trade(i):
        return {
            "TradeID": f"T{i+1}",
            "Trader": f"Trader_{random.randint(1, 5)}",
            "Instrument": "XYZ",
            "Price": round(random.uniform(101, 150), 2),
            "Quantity": random.randint(51, 100),
            "Side": random.choice(["Buy", "Sell"]),
            "simulated": True
        }

    # Generate or replicate orders
    if orders_df is not None and not orders_df.empty:
        orders_df = orders_df.copy()
        orders_df["simulated"] = True
        orders_df["Price"] = orders_df["Price"].apply(lambda x: max(x, 101))
        orders_df["BaseCcyQty"] = orders_df["BaseCcyQty"].apply(lambda x: max(x, 51))
        orders_df = pd.concat([orders_df] * (order_count // len(orders_df) + 1), ignore_index=True).iloc[:order_count]
    else:
        orders_df = pd.DataFrame([generate_order(i) for i in range(order_count)])

    # Generate or replicate trades
    if trades_df is not None and not trades_df.empty:
        trades_df = trades_df.copy()
        trades_df["simulated"] = True
        trades_df["Price"] = trades_df["Price"].apply(lambda x: max(x, 101))
        trades_df["Quantity"] = trades_df["Quantity"].apply(lambda x: max(x, 51))
        trades_df = pd.concat([trades_df] * (trade_count // len(trades_df) + 1), ignore_index=True).iloc[:trade_count]
    else:
        trades_df = pd.DataFrame([generate_trade(i) for i in range(trade_count)])

    # Market depth remains unchanged
    if market_depth_df is not None:
        market_depth_df = market_depth_df.copy()
        market_depth_df["simulated"] = True

    return orders_df, trades_df, market_depth_df
