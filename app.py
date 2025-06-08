import streamlit as st
import pandas as pd
from data_generator import generate_orders, generate_trades, generate_market_depth
from rule_engine import SmokingRuleEngine, Order, MarketDepth

# Streamlit UI setup
st.set_page_config(page_title="Market Abuse Scenario Simulator", layout="wide")
st.title("Market Abuse Scenario Simulator")

st.markdown("""
This app simulates synthetic market data (orders, trades, and market depth) and applies a rule engine to detect potential market abuse scenarios such as 'Smoking'.
""")

# Sidebar configuration
st.sidebar.header("Simulation Settings")
num_orders = st.sidebar.slider("Number of Orders", min_value=5, max_value=100, value=10)
num_trades = st.sidebar.slider("Number of Trades", min_value=1, max_value=50, value=5)

st.sidebar.markdown("### Or Upload Your Own Data")
uploaded_orders = st.sidebar.file_uploader("Upload Orders CSV", type=["csv"])
uploaded_depth = st.sidebar.file_uploader("Upload Market Depth CSV", type=["csv"])

# Helper functions to convert DataFrame to model objects
def df_to_orders(df):
    return [
        Order(
            OrderId=row["OrderId"],
            EventType=row["EventType"],
            Side=row["Side"],
            BaseCcyQty=row["BaseCcyQty"],
            BaseCcyLeavesQty=row["BaseCcyLeavesQty"],
            CumulativeQty=row["CumulativeQty"],
            Price=row["Price"],
            MarketId=row["MarketId"],
            InstrumentCode=row["InstrumentCode"],
            ReceivedTime=pd.to_datetime(row["ReceivedTime"])
        )
        for _, row in df.iterrows()
    ]

def df_to_market_depth(df):
    return [
        MarketDepth(
            InstrumentCode=row["InstrumentCode"],
            VenueId=row["VenueId"],
            MarketTimestamp=pd.to_datetime(row["MarketTimestamp"]),
            BookLevel=row["BookLevel"],
            Side=row["Side"],
            Price=row["Price"],
            Quantity=row["Quantity"],
            ReceivedTime=pd.to_datetime(row["ReceivedTime"]),
            FeedId=row["FeedId"],
            BaseCcyQuantity=row["BaseCcyQuantity"]
        )
        for _, row in df.iterrows()
    ]

# Run simulation
if st.sidebar.button("Run Simulation"):
    # Use uploaded or synthetic data
    if uploaded_orders is not None:
        orders_df = pd.read_csv(uploaded_orders)
        orders = df_to_orders(orders_df)
        st.subheader("Uploaded Orders")
        st.dataframe(orders_df)
    else:
        orders = generate_orders(num_orders)
        st.subheader("Generated Orders")
        st.dataframe(pd.DataFrame([o.__dict__ for o in orders]))

    if uploaded_depth is not None:
        depth_df = pd.read_csv(uploaded_depth)
        market_depth = df_to_market_depth(depth_df)
        st.subheader("Uploaded Market Depth")
        st.dataframe(depth_df)
    else:
        market_depth = generate_market_depth()
        st.subheader("Generated Market Depth")
        st.dataframe(pd.DataFrame([d.__dict__ for d in market_depth]))

    trades = generate_trades(num_trades)
    st.subheader("Generated Trades")
    st.dataframe(pd.DataFrame([t.__dict__ for t in trades]))

    # Evaluate alerts
    engine = SmokingRuleEngine()
    alerts = engine.evaluate(orders, trades, market_depth)
    alerts_df = pd.DataFrame(alerts)

    st.subheader("Generated Alerts")
    if not alerts_df.empty:
        st.dataframe(alerts_df)
        csv = alerts_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Alerts as CSV", data=csv, file_name="alerts.csv", mime="text/csv")
    else:
        st.info("No alerts generated based on the current simulation.")
else:
    st.info("Adjust the settings in the sidebar and click 'Run Simulation' to begin.")
