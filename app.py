import streamlit as st
import pandas as pd
from datetime import datetime
import dataclasses
import json
from rule_engine import SmokingRuleEngine, Order, Trade, MarketDepth
from data_generator import simulate_data

st.title("Test Data Simulator for Market Abuse Scenarios")

# Sidebar inputs
st.sidebar.header("Upload Input Data")
order_file = st.sidebar.file_uploader("Upload Order Data (CSV)", type="csv")
trade_file = st.sidebar.file_uploader("Upload Trade Data (CSV)", type="csv")
depth_file = st.sidebar.file_uploader("Upload Market Depth Data (CSV)", type="csv")

order_count = st.sidebar.number_input("Number of Orders to Simulate", min_value=1, value=10)
trade_count = st.sidebar.number_input("Number of Trades to Simulate", min_value=1, value=10)
include_trades = st.sidebar.checkbox("Include Trades in Alert Evaluation", value=True)
generate_button = st.sidebar.button("Generate Alert-Triggering Data")

# Read uploaded files
def read_csv(file):
    if file is not None:
        return pd.read_csv(file)
    return None

orders_df = read_csv(order_file)
trades_df = read_csv(trade_file)
depth_df = read_csv(depth_file)

# Preview uploaded data
st.header("Uploaded Data Preview")
if orders_df is not None and not orders_df.empty:
    st.subheader("Orders")
    st.dataframe(orders_df)
if trades_df is not None and not trades_df.empty:
    st.subheader("Trades")
    st.dataframe(trades_df)
if depth_df is not None and not depth_df.empty:
    st.subheader("Market Depth")
    st.dataframe(depth_df)

# Helper to convert DataFrame to dataclass list
def convert_to_dataclass_list(df, cls):
    if df is None or df.empty:
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

# Generate and evaluate
if generate_button:
    st.header("Simulated Data and Alerts")
    simulated_orders, simulated_trades, simulated_depth = simulate_data(
        order_count=order_count,
        trade_count=trade_count,
        orders_df=orders_df,
        trades_df=trades_df,
        market_depth_df=depth_df
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

    if simulated_depth is not None and not simulated_depth.empty:
        st.subheader("Simulated Market Depth")
        st.dataframe(simulated_depth)
        csv = simulated_depth.to_csv(index=False).encode('utf-8')
        st.download_button("Download Simulated Market Depth", csv, "simulated_depth.csv", "text/csv")

    st.subheader("Generated Alerts")
    try:
        orders_list = convert_to_dataclass_list(simulated_orders, Order)
        trades_list = convert_to_dataclass_list(simulated_trades, Trade) if include_trades else []
        depth_list = convert_to_dataclass_list(simulated_depth, MarketDepth)

        class SmokingRuleEngineWithDetails(SmokingRuleEngine):
            def evaluate_alerts(self, orders, trades, market_depth):
                alerts = []
                for order in orders:
                    if order.Price > 100 and order.BaseCcyQty > 50:
                        alerts.append({
                            "Alert ID": f"A-{order.OrderId}",
                            "Type": "Smoking",
                            "Triggered By": "Order",
                            "Instrument": order.InstrumentCode,
                            "Market": order.MarketId,
                            "Time": order.ReceivedTime,
                            "Triggering Order": json.dumps(order.__dict__, default=str)
                        })
                if self.trade_inclusion_flag:
                    for trade in trades:
                        if trade.Price > 100 and trade.Quantity > 50:
                            alerts.append({
                                "Alert ID": f"T-{trade.TradeId}",
                                "Type": "Smoking",
                                "Triggered By": "Trade",
                                "Instrument": trade.InstrumentCode,
                                "Market": trade.MarketId,
                                "Time": trade.TradeTime,
                                "Triggering Trade": json.dumps(trade.__dict__, default=str)
                            })
                return pd.DataFrame(alerts)

        engine = SmokingRuleEngineWithDetails(trade_inclusion_flag=include_trades)
        alerts = engine.evaluate_alerts(orders_list, trades_list, depth_list)

        if alerts is not None and not alerts.empty:
            for _, row in alerts.iterrows():
                with st.expander(f"Alert {row['Alert ID']} - {row['Type']}"):
                    st.write("**Triggered By:**", row["Triggered By"])
                    st.write("**Instrument:**", row["Instrument"])
                    st.write("**Market:**", row["Market"])
                    st.write("**Time:**", row["Time"])
                    if row["Triggered By"] == "Order":
                        st.json(json.loads(row["Triggering Order"]))
                    elif row["Triggered By"] == "Trade":
                        st.json(json.loads(row["Triggering Trade"]))

            csv = alerts.to_csv(index=False).encode('utf-8')
            st.download_button("Download Alerts", csv, "alerts.csv", "text/csv")
        else:
            st.info("No alerts generated.")
    except Exception as e:
        st.error(f"Error during alert evaluation: {e}")
