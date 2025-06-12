import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

# Load uploaded files
orders_df = pd.read_csv("Test_orders.csv")
trades_df = pd.read_csv("Test_Trade.csv")
depth_df = pd.read_csv("Test_MarketDepth.csv")

# Normalize timestamps
def parse_time(ts):
    try:
        return pd.to_datetime(ts)
    except:
        return datetime.now()

orders_df['ReceivedTime'] = orders_df['ReceivedTime'].apply(parse_time)
trades_df['ReceivedTime'] = trades_df['ReceivedTime'].apply(parse_time)
depth_df['ReceivedTime'] = depth_df['ReceivedTime'].apply(parse_time)
depth_df['MarketTimestamp'] = depth_df['MarketTimestamp'].apply(parse_time)

# Simulate alert-triggering order + depth
def simulate_alert_orders(orders_df, depth_df):
    base_columns = orders_df.columns
    simulated_orders = []

    # Near-side Buy order
    near_order = orders_df.iloc[0].copy()
    near_order['OrderId'] = str(uuid.uuid4())
    near_order['EventType'] = 'Filled'
    near_order['Side'] = 'Buy'
    near_order['BaseCcyQty'] = 2_000_000
    near_order['BaseCcyLeavesQty'] = 0
    near_order['CumulativeQty'] = 2_000_000
    near_order['Price'] = 100.0
    near_order['ReceivedTime'] = datetime.now()

    # Far-side Sell order
    far_order = orders_df.iloc[0].copy()
    far_order['OrderId'] = str(uuid.uuid4())
    far_order['EventType'] = 'New'
    far_order['Side'] = 'Sell'
    far_order['BaseCcyQty'] = 500_000
    far_order['BaseCcyLeavesQty'] = 500_000
    far_order['CumulativeQty'] = 0
    far_order['Price'] = 99.5
    far_order['ReceivedTime'] = near_order['ReceivedTime'] + timedelta(seconds=10)

    simulated_orders.append(near_order)
    simulated_orders.append(far_order)

    return pd.DataFrame(simulated_orders)[base_columns]

# Simulate alert-triggering trade + depth
def simulate_alert_trades(trades_df, depth_df):
    base_columns = trades_df.columns
    simulated_trades = []

    # Near-side Buy trade
    near_trade = trades_df.iloc[0].copy()
    near_trade['TradeId'] = str(uuid.uuid4())
    near_trade['EventType'] = 'TN'
    near_trade['Side'] = 'Buy'
    near_trade['BaseCcyValue'] = 2_000_000
    near_trade['Price'] = 100.0
    near_trade['ReceivedTime'] = datetime.now()

    simulated_trades.append(near_trade)

    return pd.DataFrame(simulated_trades)[base_columns]

# Simulate alert-triggering market depth
def simulate_alert_depth(depth_df):
    base_columns = depth_df.columns
    simulated_depth = []

    # Best bid
    bid = depth_df.iloc[0].copy()
    bid['Side'] = 'Buy'
    bid['Price'] = 99.0
    bid['Quantity'] = 100000
    bid['BookLevel'] = 1
    bid['MarketTimestamp'] = datetime.now()
    bid['ReceivedTime'] = datetime.now()

    # Best ask
    ask = depth_df.iloc[0].copy()
    ask['Side'] = 'Sell'
    ask['Price'] = 101.0
    ask['Quantity'] = 100000
    ask['BookLevel'] = 1
    ask['MarketTimestamp'] = datetime.now()
    ask['ReceivedTime'] = datetime.now()

    simulated_depth.append(bid)
    simulated_depth.append(ask)

    return pd.DataFrame(simulated_depth)[base_columns]

# Simulate based on trade inclusion flag
trade_inclusion_flag = True  # Toggle this to False to simulate only orders + depth

if trade_inclusion_flag:
    simulated_orders = simulate_alert_orders(orders_df, depth_df)
    simulated_trades = simulate_alert_trades(trades_df, depth_df)
    simulated_depth = simulate_alert_depth(depth_df)
else:
    simulated_orders = simulate_alert_orders(orders_df, depth_df)
    simulated_trades = pd.DataFrame(columns=trades_df.columns)
    simulated_depth = simulate_alert_depth(depth_df)

# Save simulated data
simulated_orders.to_csv("simulated_orders.csv", index=False)
simulated_trades.to_csv("simulated_trades.csv", index=False)
simulated_depth.to_csv("simulated_market_depth.csv", index=False)

print("Simulated alert-triggering data generated and saved.")

