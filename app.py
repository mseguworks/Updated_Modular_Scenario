import streamlit as st
import pandas as pd
from rule_engine import SmokingRuleEngine
from data_generator import simulate_data

# Streamlit App Title
st.title("Cloud-Hosted Trade Surveillance Test Platform")

# Sidebar for file uploads and toggle
st.sidebar.header("Upload Input Data")
order_file = st.sidebar.file_uploader("Upload Order Data (CSV)", type="csv")
trade_file = st.sidebar.file_uploader("Upload Trade Data (CSV)", type="csv")
depth_file = st.sidebar.file_uploader("Upload Market Depth Data (CSV)", type="csv")
include_trades = st.sidebar.checkbox("Include Trades in Alert Evaluation", value=True)
generate_button = st.sidebar.button("Generate Alert-Triggering Data")

# Function to read uploaded CSVs
def read_csv(file):
    if file is not None:
        return pd.read_csv(file)
    return None

# Read uploaded files
orders_df = read_csv(order_file)
trades_df = read_csv(trade_file)
depth_df = read_csv(depth_file)

# Display uploaded data
st.header("Uploaded Data Preview")
if orders_df is not None:
    st.subheader("Orders")
    st.dataframe(orders_df)
if trades_df is not None:
    st.subheader("Trades")
    st.dataframe(trades_df)
if depth_df is not None:
    st.subheader("Market Depth")
    st.dataframe(depth_df)

# Generate and display simulated data and alerts
if generate_button:
    st.header("Simulated Data and Alerts")

    # Simulate data
    simulated_orders, simulated_trades, simulated_depth = simulate_data(
        orders_df, trades_df, depth_df, include_trades
    )

    # Display simulated data
    if simulated_orders is not None and not simulated_orders.empty:
        st.subheader("Simulated Orders")
        st.dataframe(simulated_orders)
        csv = simulated_orders.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Orders", csv, "simulated_orders.csv", "text/csv")

    if include_trades and simulated_trades is not None and not simulated_trades.empty:
        st.subheader("Simulated Trades")
        st.dataframe(simulated_trades)
        csv = simulated_trades.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Trades", csv, "simulated_trades.csv", "text/csv")

    if simulated_depth is not None and not simulated_depth.empty:
        st.subheader("Simulated Market Depth")
        st.dataframe(simulated_depth)
        csv = simulated_depth.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Market Depth", csv, "simulated_depth.csv", "text/csv")

    # Evaluate alerts
    st.subheader("Generated Alerts")
    engine = SmokingRuleEngine(trade_inclusion_flag=include_trades)
    alerts = engine.evaluate_alerts(simulated_orders, simulated_trades, simulated_depth)
    if alerts is not None and not alerts.empty:
        st.dataframe(alerts)
        csv = alerts.to_csv(index=False).encode('utf-8')
        st.download_button("Download Alerts", csv, "alerts.csv", "text/csv")
    else:
        st.info("No alerts generated.")
