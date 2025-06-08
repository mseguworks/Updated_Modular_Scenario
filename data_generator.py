# Regenerate data_generator.py and requirements.txt for Streamlit deployment

# Write the updated data_generator.py file
data_generator_code = '''import random
import datetime
from rule_engine import Order, Trade, MarketDepth

def generate_orders(n=10):
    sides = ['Buy', 'Sell']
    events = ['Filled', 'Partially Filled']
    orders = []
    for i in range(n):
        side = random.choice(sides)
        event = random.choice(events)
        qty = random.uniform(1_000_000, 10_000_000)
        leaves = qty * random.uniform(0.1, 0.5) if event == 'Partially Filled' else 0
        orders.append(Order(
            OrderId=f"O{i}",
            EventType=event,
            Side=side,
            BaseCcyQty=qty,
            BaseCcyLeavesQty=leaves,
            CumulativeQty=qty - leaves,
            Price=random.uniform(99, 101),
            MarketId="LSE",
            InstrumentCode="XYZ",
            ReceivedTime=datetime.datetime.now() + datetime.timedelta(seconds=i)
        ))
    return orders

def generate_trades(n=5):
    sides = ['Buy', 'Sell']
    trades = []
    for i in range(n):
        side = random.choice(sides)
        trades.append(Trade(
            TradeId=f"T{i}",
            EventType='TN',
            Side=side,
            BaseCcyValue=random.uniform(1_000_000, 10_000_000),
            Price=random.uniform(99, 101),
            MarketId="LSE",
            InstrumentCode="XYZ",
            ReceivedTime=datetime.datetime.now() + datetime.timedelta(seconds=i)
        ))
    return trades

def generate_market_depth():
    depth = []
    for side in ['Buy', 'Sell']:
        for level in range(1, 3):
            depth.append(MarketDepth(
                InstrumentCode="XYZ",
                VenueId="LSE",
                MarketTimestamp=datetime.datetime.now(),
                BookLevel=level,
                Side=side,
                Price=100.0 + (0.01 * level if side == 'Buy' else -0.01 * level),
                Quantity=1_000_000,
                ReceivedTime=datetime.datetime.now(),
                FeedId="MD1",
                BaseCcyQuantity=1_000_000
            ))
    return depth
'''

with open("data_generator.py", "w") as f:
    f.write(data_generator_code)

# Write the updated requirements.txt file
requirements = '''streamlit
pandas
'''

with open("requirements.txt", "w") as f:
    f.write(requirements)

print("Updated data_generator.py and requirements.txt have been generated.")

