import pandas as pd
import numpy as np

def simulate_data(orders_df=None, trades_df=None, depth_df=None, include_trades=True):
    """
    Simulates alert-triggering data from uploaded orders and market depth.
    Adjusts prices and quantities to meet alert thresholds.
    """
    simulated_orders = pd.DataFrame()
    simulated_trades = pd.DataFrame()
    simulated_depth = pd.DataFrame()

    # Simulate orders
    if orders_df is not None and not orders_df.empty:
        simulated_orders = orders_df.copy()
        simulated_orders["Price"] = 105.0  # Ensure price > 100
        simulated_orders["BaseCcyQty"] = 100.0  # Ensure quantity > 50
        simulated_orders["BaseCcyLeavesQty"] = 50.0
        simulated_orders["CumulativeQty"] = 50.0
        simulated_orders["simulated"] = True

    # Simulate trades only if include_trades is True and trades_df is provided
    if include_trades and trades_df is not None and not trades_df.empty:
        simulated_trades = trades_df.copy()
        simulated_trades["Price"] = 105.0
        simulated_trades["Quantity"] = 100.0
        simulated_trades["simulated"] = True

    # Simulate market depth
    if depth_df is not None and not depth_df.empty:
        simulated_depth = depth_df.copy()
        if "bid_price" in simulated_depth.columns:
            simulated_depth["bid_price"] = simulated_depth["bid_price"] * np.random.uniform(0.98, 1.02, len(simulated_depth))
        if "ask_price" in simulated_depth.columns:
            simulated_depth["ask_price"] = simulated_depth["ask_price"] * np.random.uniform(0.98, 1.02, len(simulated_depth))
        simulated_depth["simulated"] = True

    return simulated_orders, simulated_trades, simulated_depth
