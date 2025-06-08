from rule_engine import SmokingRuleEngine
from data_generator import generate_orders, generate_trades, generate_market_depth
import pandas as pd

# Generate synthetic data
orders = generate_orders(10)
trades = generate_trades(5)
market_depth = generate_market_depth()

# Initialize rule engine
engine = SmokingRuleEngine()

# Evaluate alerts
alerts = engine.evaluate(orders, trades, market_depth)

# Convert to DataFrame and save
df = pd.DataFrame(alerts)
df.to_csv("alerts.csv", index=False)

print("Alerts generated and saved to alerts.csv")
