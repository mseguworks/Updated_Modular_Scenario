import streamlit as st
import pandas as pd
from data_generator import generate_orders, generate_trades, generate_market_depth, generate_orders_from_uploaded_data
from rule_engine import SmokingRuleEngine, Order, Trade, MarketDepth

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
intensity = st.sidebar.slider("Intensity (Variability)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)

st.sidebar.markdown("### Or Upload Your Own Data")
uploaded_orders = st.sidebar.file_uploader("Upload Orders CSV", type=["csv"])
uploaded_depth = st.sidebar.file_uploader("Upload Market Depth CSV", type=["csv"])

# Run simulation
if st.sidebar.button("Run Simulation"):
    # Use uploaded or synthetic orders
    if uploaded_orders is not None:
        orders_df = pd.read_csv(uploaded_orders)
        st.subheader("Uploaded Orders")
        st.dataframe(orders_df)
        orders = generate_orders_from_uploaded_data(orders_df, num_orders, intensity)
    else:
        orders = pd.DataFrame(generate_orders(num_orders))
        st.subheader("Generated Orders")
        st.dataframe(orders)

    # Use uploaded or synthetic market depth
    if uploaded_depth is not None:
        depth_df = pd.read_csv(uploaded_depth)
        st.subheader("Uploaded Market Depth")
        st.dataframe(depth_df)
        market_depth = depth_df.to_dict(orient="records")
    else:
        market_depth = generate_market_depth()
        st.subheader("Generated Market Depth")
        st.dataframe(pd.DataFrame(market_depth))

    # Generate trades
    trades = generate_trades(num_trades)
    st.subheader("Generated Trades")
    st.dataframe(pd.DataFrame(trades))

    # Evaluate alerts
    engine = SmokingRuleEngine()
    try:
        orders_list = [Order(**o) for o in orders.to_dict(orient="records")]
        trades_list = [Trade(**t) for t in trades]
        depth_list = [MarketDepth(**d) for d in market_depth]

        alerts = engine.evaluate(orders_list, trades_list, depth_list)
        alerts_df = pd.DataFrame(alerts)

        st.subheader("Generated Alerts")
        if not alerts_df.empty:
            st.dataframe(alerts_df)
            csv = alerts_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Alerts as CSV", data=csv, file_name="alerts.csv", mime="text/csv")
        else:
            st.info("No alerts generated based on the current simulation.")
    except Exception as e:
        st.error(f"Error during alert evaluation: {e}")
else:
    st.info("Adjust the settings in the sidebar and click 'Run Simulation' to begin.")
