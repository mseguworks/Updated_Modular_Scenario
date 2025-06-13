import pandas as pd

def simulate_data(order_count=10, trade_count=10, orders_df=None, trades_df=None, market_depth_df=None):
    # Adjust orders to meet alert-triggering thresholds
    if orders_df is not None and not orders_df.empty:
        orders_df = orders_df.copy()
        orders_df["simulated"] = True
        if "Price" in orders_df.columns:
            orders_df["Price"] = orders_df["Price"].apply(lambda x: max(x, 101))
        if "BaseCcyQty" in orders_df.columns:
            orders_df["BaseCcyQty"] = orders_df["BaseCcyQty"].apply(lambda x: max(x, 51))
        if len(orders_df) < order_count:
            orders_df = pd.concat([orders_df] * (order_count // len(orders_df) + 1), ignore_index=True).iloc[:order_count]
        else:
            orders_df = orders_df.sample(n=order_count, random_state=1).reset_index(drop=True)

    # Adjust trades to meet alert-triggering thresholds
    if trades_df is not None and not trades_df.empty:
        trades_df = trades_df.copy()
        trades_df["simulated"] = True
        if "Price" in trades_df.columns:
            trades_df["Price"] = trades_df["Price"].apply(lambda x: max(x, 101))
        if "Quantity" in trades_df.columns:
            trades_df["Quantity"] = trades_df["Quantity"].apply(lambda x: max(x, 51))
        if len(trades_df) < trade_count:
            trades_df = pd.concat([trades_df] * (trade_count // len(trades_df) + 1), ignore_index=True).iloc[:trade_count]
        else:
            trades_df = trades_df.sample(n=trade_count, random_state=1).reset_index(drop=True)

    # Mark market depth as simulated if provided
    if market_depth_df is not None and not market_depth_df.empty:
        market_depth_df = market_depth_df.copy()
        market_depth_df["simulated"] = True

    return orders_df, trades_df, market_depth_df
