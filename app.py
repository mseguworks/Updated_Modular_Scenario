import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from rule_engine import SmokingRuleEngine, Order, Trade, MarketDepth
from data_generator import simulate_data
import dataclasses

st.title("Test Data Simulator for Market Abuse Scenarios")

st.sidebar.header("Upload Input Data")
order_file = st.sidebar.file_uploader("Upload Order Data (CSV)", type="csv")
trade_file = st.sidebar.file_uploader("Upload Trade Data (CSV)", type="csv")
depth_file = st.sidebar.file_uploader("Upload Market Depth Data (CSV)", type="csv")
include_trades = st.sidebar.checkbox("Include Trades in Alert Evaluation", value=True)
generate_button = st.sidebar.button("Generate Alert-Triggering Data")

def read_csv(file):
    if file is not None:
        return pd.read_csv(file)
    return pd.DataFrame()

orders_df = read_csv(order_file)
trades_df = read_csv(trade_file)
depth_df = read_csv(depth_file)

st.header("Uploaded Data Preview")
if not orders_df.empty:
    st.subheader("Orders")
    st.dataframe(orders_df)
if not trades_df.empty:
    st.subheader("Trades")
    st.dataframe(trades_df)
if not depth_df.empty:
    st.subheader("Market Depth")
    st.dataframe(depth_df)

def convert_to_dataclass_list(df, cls):
    if df.empty:
        return []
    field_names = {f.name for f in dataclasses.fields(cls)}
    records = df.to_dict(orient="records")
    cleaned = []
    for row in records:
        filtered = {k: v for k, v in row.items() if k in field_names}
        for f in dataclasses.fields(cls):
            if f.name not in filtered:
                filtered[f.name] = None
            elif f.type == datetime and not isinstance(filtered[f.name], datetime):
                try:
                    filtered[f.name] = pd.to_datetime(filtered[f.name])
                except:
                    filtered[f.name] = None
        cleaned.append(cls(**filtered))
    return cleaned

if generate_button:
    st.header("Simulated Data and Alerts")

    simulated_orders, simulated_trades, simulated_depth = simulate_data(
        orders_df, trades_df, depth_df, include_trades
    )

    if not simulated_orders.empty:
        st.subheader("Simulated Orders")
        st.dataframe(simulated_orders)
        csv = simulated_orders.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Orders", csv, "simulated_orders.csv", "text/csv")

    if include_trades and not simulated_trades.empty:
        st.subheader("Simulated Trades")
        st.dataframe(simulated_trades)
        csv = simulated_trades.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Trades", csv, "simulated_trades.csv", "text/csv")

    if not simulated_depth.empty:
        st.subheader("Simulated Market Depth")
        st.dataframe(simulated_depth)
        csv = simulated_depth.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Market Depth", csv, "simulated_depth.csv", "text/csv")

    st.subheader("Generated Alerts")
    try:
        orders_list = convert_to_dataclass_list(simulated_orders, Order)
        trades_list = convert_to_dataclass_list(simulated_trades, Trade) if include_trades else []
        depth_list = convert_to_dataclass_list(simulated_depth, MarketDepth)

        engine = SmokingRuleEngine(trade_inclusion_flag=include_trades)
        alerts = engine.evaluate_alerts(orders_list, trades_list, depth_list)

        if alerts is not None and not alerts.empty:
            st.dataframe(alerts)
            csv = alerts.to_csv(index=False).encode('utf-8')
            st.download_button("Download Alerts", csv, "alerts.csv", "text/csv")
        else:
            st.info("No alerts generated.")
    except Exception as e:
        st.error(f"Error during alert evaluation: {e}")
