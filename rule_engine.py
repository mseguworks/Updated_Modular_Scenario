from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import pandas as pd

@dataclass(frozen=True)
class Order:
    OrderId: str
    EventType: str
    Side: str
    BaseCcyQty: float
    BaseCcyLeavesQty: float
    CumulativeQty: float
    Price: float
    MarketId: str
    InstrumentCode: str
    ReceivedTime: datetime
    SeqNum: Optional[int] = None

@dataclass(frozen=True)
class Trade:
    TradeId: str
    Side: str
    Price: float
    Quantity: float
    MarketId: str
    InstrumentCode: str
    TradeTime: datetime
    SeqNum: Optional[int] = None

@dataclass(frozen=True)
class MarketDepth:
    MarketId: str
    InstrumentCode: str
    bid_price: float
    ask_price: float
    DepthTime: datetime

class SmokingRuleEngine:
    def __init__(self, trade_inclusion_flag=True):
        self.trade_inclusion_flag = trade_inclusion_flag

    def evaluate_alerts(self, orders: List[Order], trades: List[Trade], depth: List[MarketDepth]) -> pd.DataFrame:
        alerts = []

        for order in orders:
            if order.Price > 100 and order.BaseCcyQty > 50:
                alerts.append({
                    "Alert ID": f"A-{order.OrderId}",
                    "Type": "Smoking",
                    "Triggered By": "Order",
                    "Instrument": order.InstrumentCode,
                    "Market": order.MarketId,
                    "Time": order.ReceivedTime
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
                        "Time": trade.TradeTime
                    })

        return pd.DataFrame(alerts)
