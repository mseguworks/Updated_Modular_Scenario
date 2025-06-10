import streamlit as st
import pandas as pd
from data_generator import generate_orders, generate_orders_from_uploaded_data
from rule_engine import SmokingRuleEngine, Order, Trade, MarketDepth

# Streamlit UI setup
st.set_page_config(page_title="Market Abuse Scenario Simulator", layout="wide")
st.title("Market Abuse Scenario Simulator")

st.markdown("""
This app simulates synthetic market data (orders) and applies a rule engine to detect potential market abuse scenarios such as 'Smoking'.
""")

# Sidebar configuration
st.sidebar.header("Simulation Settings")
num_orders = st.sidebar.slider("Number of Orders", min_value=5, max_value=100, value=10)

st.sidebar.markdown("### Or Upload Your Own Order Data")
uploaded_orders = st.sidebar.file_uploader("Upload Orders CSV", type=["csv"])

# Run simulation
if st.sidebar.button("Run Simulation"):
    if uploaded_orders is not None:
        orders_df = pd.read_csv(uploaded_orders)
        st.subheader("Uploaded Orders")
        st.dataframe(orders_df)
        orders = generate_orders_from_uploaded_data(orders_df, num_orders)
        st.subheader("Simulated Orders Based on Uploaded Data")
        st.dataframe(orders)

        # Evaluate alerts
        engine = SmokingRuleEngine()
        try:
            orders_list = [Order(**o) for o in orders.to_dict(orient="records")]
            alerts = engine.evaluate(orders_list, [], [])
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
        orders = pd.DataFrame(generate_orders(num_orders))
        st.subheader("Generated Orders")
        st.dataframe(orders)

        # Generate dummy trades and market depth for evaluation
        trades = []
        market_depth = []

        # Evaluate alerts
        engine = SmokingRuleEngine()
        try:
            orders_list = [Order(**o) for o in orders.to_dict(orient="records")]
            alerts = engine.evaluate(orders_list, trades, market_depth)
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
