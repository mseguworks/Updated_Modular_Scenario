import json
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

        # Create a lookup for best bid/ask by (MarketId, InstrumentCode)
        depth_lookup = {}
        for d in depth:
            key = (d.MarketId, d.InstrumentCode)
            if key not in depth_lookup or d.DepthTime > depth_lookup[key].DepthTime:
                depth_lookup[key] = d

        for order in orders:
            alert_triggered = False
            reason = []

            if order.Price > 100 and order.BaseCcyQty > 50:
                alert_triggered = True
                reason.append("Price > 100 and BaseCcyQty > 50")

            # Market depth rule
            depth_key = (order.MarketId, order.InstrumentCode)
            if depth_key in depth_lookup:
                best_depth = depth_lookup[depth_key]
                if order.Side == "Buy" and order.Price > best_depth.ask_price:
                    alert_triggered = True
                    reason.append("Buy order price > best ask")
                elif order.Side == "Sell" and order.Price < best_depth.bid_price:
                    alert_triggered = True
                    reason.append("Sell order price < best bid")

            if alert_triggered:
                alerts.append({
                    "Alert ID": f"A-{order.OrderId}",
                    "Type": "Smoking",
                    "Triggered By": "Order",
                    "Instrument": order.InstrumentCode,
                    "Market": order.MarketId,
                    "Time": order.ReceivedTime,
                    "Reason": "; ".join(reason),
                    "Triggering Order": json.dumps(order.__dict__, default=str)
                })

        if self.trade_inclusion_flag and trades:
            for trade in trades:
                if trade.Price > 100 and trade.Quantity > 50:
                    alerts.append({
                        "Alert ID": f"T-{trade.TradeId}",
                        "Type": "Smoking",
                        "Triggered By": "Trade",
                        "Instrument": trade.InstrumentCode,
                        "Market": trade.MarketId,
                        "Time": trade.TradeTime,
                        "Reason": "Price > 100 and Quantity > 50",
                        "Triggering Trade": json.dumps(trade.__dict__, default=str)
                    })

        return pd.DataFrame(alerts)
