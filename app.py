import streamlit as st
import pandas as pd
from data_generator import generate_orders, generate_trades, generate_market_depth
from rule_engine import SmokingRuleEngine

# Streamlit UI
st.set_page_config(page_title="Market Abuse Scenario Simulator", layout="wide")
st.title("Market Abuse Scenario Simulator")

st.markdown("""
This app simulates synthetic market data (orders, trades, and market depth) and applies a rule engine to detect potential market abuse scenarios such as 'Smoking'.
""")

# Sidebar configuration
st.sidebar.header("Simulation Settings")
num_orders = st.sidebar.slider("Number of Orders", min_value=5, max_value=100, value=10)
num_trades = st.sidebar.slider("Number of Trades", min_value=1, max_value=50, value=5)

if st.sidebar.button("Run Simulation"):
    # Generate synthetic data
    orders = generate_orders(num_orders)
    trades = generate_trades(num_trades)
    market_depth = generate_market_depth()

    # Display generated data
    st.subheader("Generated Orders")
    st.dataframe(pd.DataFrame([o.__dict__ for o in orders]))

    st.subheader("Generated Trades")
    st.dataframe(pd.DataFrame([t.__dict__ for t in trades]))

    st.subheader("Generated Market Depth")
    st.dataframe(pd.DataFrame([d.__dict__ for d in market_depth]))

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
