from dataclasses import dataclass
from typing import List, Dict
import datetime


@dataclass
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
    ReceivedTime: datetime.datetime


@dataclass
class Trade:
    TradeId: str
    EventType: str
    Side: str
    BaseCcyValue: float
    Price: float
    MarketId: str
    InstrumentCode: str
    ReceivedTime: datetime.datetime


@dataclass
class MarketDepth:
    InstrumentCode: str
    VenueId: str
    MarketTimestamp: datetime.datetime
    BookLevel: int
    Side: str
    Price: float
    Quantity: float
    ReceivedTime: datetime.datetime
    FeedId: str
    BaseCcyQuantity: float


@dataclass
class Alert:
    AlertId: int
    ScenarioId: str
    AlertTimestamp: datetime.datetime
    PartyId: str
    MarketId: str
    InstrumentId: str
    Desk: str
    Trader: str
    AlertDescription: str


class SmokingRuleEngine:
    def __init__(self, trade_inclusion_flag=True, near_threshold=5_000_000, far_threshold=5_000_000,
                 lookup_window_sec=45, depth_level=1):
        self.trade_inclusion_flag = trade_inclusion_flag
        self.near_threshold = near_threshold
        self.far_threshold = far_threshold
        self.lookup_window = datetime.timedelta(seconds=lookup_window_sec)
        self.depth_level = depth_level

    def evaluate(self, orders: List[Order], trades: List[Trade], market_depth: List[MarketDepth]) -> List[Dict]:
        alerts = []
        near_side_events = []

        if self.trade_inclusion_flag:
            for trade in trades:
                if trade.EventType in ['TN', 'TR'] and trade.BaseCcyValue > self.near_threshold:
                    near_side_events.append(trade)

        for order in orders:
            if order.EventType in ['Filled', 'Partially Filled']:
                notional = order.BaseCcyQty if order.EventType == 'Filled' else order.BaseCcyQty - order.BaseCcyLeavesQty
                if notional > self.near_threshold:
                    near_side_events.append(order)

        for event in near_side_events:
            opposite_side = 'Sell' if event.Side == 'Buy' else 'Buy'
            event_time = event.ReceivedTime
            instrument = event.InstrumentCode
            venue = event.MarketId

            far_side_orders = [
                o for o in orders
                if o.Side == opposite_side and
                   o.InstrumentCode == instrument and
                   o.MarketId == venue and
                   o.ReceivedTime >= event_time and
                   o.ReceivedTime <= event_time + self.lookup_window and
                   o.BaseCcyQty <= self.far_threshold
            ]

            for far_order in far_side_orders:
                depth = [
                    d for d in market_depth
                    if d.InstrumentCode == instrument and
                       d.VenueId == venue and
                       d.BookLevel == self.depth_level
                ]
                if not depth:
                    alerts.append(self.create_alert(event, far_order, "Market depth missing"))
                    continue

                best_bid = max((d.Price for d in depth if d.Side == 'Buy'), default=None)
                best_ask = min((d.Price for d in depth if d.Side == 'Sell'), default=None)

                if event.Side == 'Buy' and far_order.Price >= (best_bid or 0):
                    alerts.append(self.create_alert(event, far_order, "Buy price >= best bid"))
                elif event.Side == 'Sell' and far_order.Price <= (best_ask or float('inf')):
                    alerts.append(self.create_alert(event, far_order, "Sell price <= best ask"))

        return alerts

    def create_alert(self, near_event, far_order, reason) -> Dict:
        return {
            'AlertId': hash((near_event, far_order)),
            'ScenarioId': 'Smoking',
            'AlertTimestamp': datetime.datetime.now(),
            'PartyId': getattr(near_event, 'PartyId', 'N/A'),
            'MarketId': near_event.MarketId,
            'InstrumentId': near_event.InstrumentCode,
            'Desk': 'N/A',
            'Trader': 'N/A',
            'AlertDescription': reason
        }

