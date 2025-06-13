import streamlit as st
import pandas as pd
from rule_engine import SmokingRuleEngine, Order, Trade, MarketDepth
from data_generator import simulate_data

st.title("Trade Surveillance Test Platform")

# Input fields for number of orders and trades to simulate
order_count = st.number_input("Number of Orders to Simulate", min_value=1, value=10)
trade_count = st.number_input("Number of Trades to Simulate", min_value=1, value=10)

# File uploaders
orders_file = st.file_uploader("Upload Orders CSV", type="csv")
trades_file = st.file_uploader("Upload Trades CSV", type="csv")
market_depth_file = st.file_uploader("Upload Market Depth CSV", type="csv")

# Read uploaded files
orders_df = pd.read_csv(orders_file) if orders_file else None
trades_df = pd.read_csv(trades_file) if trades_file else None
market_depth_df = pd.read_csv(market_depth_file) if market_depth_file else None

# Checkbox to include trades in alert evaluation
include_trades = st.checkbox("Include Trades in Alert Evaluation", value=True)

# Simulate data
if st.button("Simulate Alert-Triggering Data"):
    orders_df, trades_df, market_depth_df = simulate_data(
        order_count=order_count,
        trade_count=trade_count,
        orders_df=orders_df,
        trades_df=trades_df,
        market_depth_df=market_depth_df
    )

    st.subheader("Simulated Orders")
    st.dataframe(orders_df)

    st.subheader("Simulated Trades")
    st.dataframe(trades_df)

    st.subheader("Simulated Market Depth")
    if market_depth_df is not None:
        st.dataframe(market_depth_df)

    # Convert to dataclass objects
    orders = [Order(**row) for row in orders_df.to_dict(orient="records")]
    trades = [Trade(**row) for row in trades_df.to_dict(orient="records")] if include_trades else []
    market_depth = [MarketDepth(**row) for row in market_depth_df.to_dict(orient="records")] if market_depth_df is not None else []

    # Run rule engine
    engine = SmokingRuleEngine(trade_inclusion_flag=include_trades)
    alerts_df = engine.evaluate_alerts(orders, trades, market_depth)

    st.subheader("Generated Alerts")
    st.dataframe(alerts_df)

    # Download buttons
    st.download_button("Download Simulated Orders", orders_df.to_csv(index=False), "simulated_orders.csv")
    st.download_button("Download Simulated Trades", trades_df.to_csv(index=False), "simulated_trades.csv")
    st.download_button("Download Alerts", alerts_df.to_csv(index=False), "alerts.csv")
