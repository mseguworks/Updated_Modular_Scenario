# Rewriting data_generator.py to contain only the simulate_data function with no top-level code

import pandas as pd
import numpy as np

def simulate_data(orders_df=None, trades_df=None, depth_df=None, include_trades=True):
    """
    Simulates alert-triggering data based on uploaded inputs and trade inclusion toggle.

    Parameters:
    - orders_df (pd.DataFrame): Uploaded order data
    - trades_df (pd.DataFrame): Uploaded trade data
    - depth_df (pd.DataFrame): Uploaded market depth data
    - include_trades (bool): Whether to include trades in alert evaluation

    Returns:
    - simulated_orders (pd.DataFrame)
    - simulated_trades (pd.DataFrame)
    - simulated_depth (pd.DataFrame)
    """

    simulated_orders = pd.DataFrame()
    simulated_trades = pd.DataFrame()
    simulated_depth = pd.DataFrame()

    # Simulate orders if orders_df is provided
    if orders_df is not None and not orders_df.empty:
        simulated_orders = orders_df.copy()
        simulated_orders["simulated"] = True
        if "price" not in simulated_orders.columns:
            simulated_orders["price"] = np.random.uniform(10, 100, len(simulated_orders))
        if "quantity" not in simulated_orders.columns:
            simulated_orders["quantity"] = np.random.randint(10, 1000, len(simulated_orders))
        simulated_orders["price"] = simulated_orders["price"] * np.random.uniform(0.95, 1.05, len(simulated_orders))
        simulated_orders["quantity"] = simulated_orders["quantity"] + np.random.randint(-10, 10, len(simulated_orders))
        simulated_orders["notional"] = simulated_orders["price"] * simulated_orders["quantity"]

    # Simulate trades if trades_df is provided and toggle is enabled
    if include_trades and trades_df is not None and not trades_df.empty:
        simulated_trades = trades_df.copy()
        simulated_trades["simulated"] = True
        if "price" not in simulated_trades.columns:
            simulated_trades["price"] = np.random.uniform(10, 100, len(simulated_trades))
        if "quantity" not in simulated_trades.columns:
            simulated_trades["quantity"] = np.random.randint(10, 1000, len(simulated_trades))
        simulated_trades["price"] = simulated_trades["price"] * np.random.uniform(0.95, 1.05, len(simulated_trades))
        simulated_trades["quantity"] = simulated_trades["quantity"] + np.random.randint(-5, 5, len(simulated_trades))
        simulated_trades["notional"] = simulated_trades["price"] * simulated_trades["quantity"]

    # Simulate market depth if depth_df is provided
    if depth_df is not None and not depth_df.empty:
        simulated_depth = depth_df.copy()
        simulated_depth["simulated"] = True
        if "bid_price" in simulated_depth.columns:
            simulated_depth["bid_price"] = simulated_depth["bid_price"] * np.random.uniform(0.98, 1.02, len(simulated_depth))
        else:
            simulated_depth["bid_price"] = np.random.uniform(10, 50, len(simulated_depth))
        if "ask_price" in simulated_depth.columns:
            simulated_depth["ask_price"] = simulated_depth["ask_price"] * np.random.uniform(0.98, 1.02, len(simulated_depth))
        else:
            simulated_depth["ask_price"] = simulated_depth["bid_price"] + np.random.uniform(0.1, 0.5, len(simulated_depth))

    return simulated_orders, simulated_trades, simulated_depth

