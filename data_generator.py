import random
import datetime
import pandas as pd

# Define functions to generate synthetic data for Orders, Trades, and Market Depth

def generate_orders(n=10):
    orders = []
    for i in range(n):
        now = datetime.datetime.now()
        qty = round(random.uniform(1_000_000, 10_000_000), 8)
        leaves_qty = round(qty * random.uniform(0.1, 0.5), 8)
        cumulative_qty = qty - leaves_qty
        fill_qty = cumulative_qty
        fill_price = round(random.uniform(99, 101), 7)
        base_ccy_qty = qty
        base_ccy_leaves_qty = leaves_qty
        base_ccy_value = round(qty * fill_price, 8)

        order = {
            "SeqNum": i,
            "OrderDetailsId": i + 1000,
            "OrderId": f"O{i}",
            "VersionId": f"V{i}",
            "EventType": random.choice(["Filled", "Partially Filled"]),
            "Type": "Limit",
            "OrderFeedId": "OF1",
            "TimeInForce": "GTC",
            "InitialTime": now,
            "OrderTime": now,
            "ExecutionTime": now,
            "CurrencyPair": "EUR/USD",
            "InstrumentCode": "XYZ",
            "SecurityClassId": "SC1",
            "AssetClassId": "AC1",
            "DealtCurrency": "EUR",
            "Price": fill_price,
            "Qty": qty,
            "LeavesQty": leaves_qty,
            "CumulativeQty": cumulative_qty,
            "FillQty": fill_qty,
            "FillPrice": fill_price,
            "PartyId": f"Party{i}",
            "SalesBookId": f"SB{i}",
            "Side": random.choice(["Buy", "Sell"]),
            "Trader": f"Trader{i}",
            "IsParent": "N",
            "ParentId": None,
            "IsAmended": "N",
            "AmendedTime": None,
            "IsCancelled": "N",
            "CancelledTime": None,
            "IsMonitored": "Y",
            "IsClientOrder": "Y",
            "BaseCcyQty": base_ccy_qty,
            "ReceivedTime": now,
            "OrigCurrencyPair": "EUR/USD",
            "OrigPrice": fill_price,
            "OrigSide": "Buy",
            "OrderFeedCounter": str(i),
            "OrderAltId": f"Alt{i}",
            "OrigOrderId": f"O{i-1}" if i > 0 else None,
            "ClientOrderId": f"CO{i}",
            "OrigClientOrderId": f"CO{i-1}" if i > 0 else None,
            "ExpireTime": now + datetime.timedelta(days=1),
            "MarketId": "LSE",
            "MaturityDate": now.date(),
            "StrikePrice": None,
            "PutCall": None,
            "PartyType": "Institution",
            "Desk": "Desk1",
            "Value": base_ccy_value,
            "BaseCcyValue": base_ccy_value,
            "OrderBookPartyId": f"OBP{i}",
            "OrderAttrib1": None,
            "OrderAttrib2": None,
            "OrderAttrib3": None,
            "OrderAttrib4": None,
            "OrderAttrib5": None,
            "OrderAttrib6": None,
            "OrderAttrib7": None,
            "OrderAttrib8": None,
            "Comments": None,
            "DimPartyId": None,
            "DimDeskId": None,
            "DimTraderId": None,
            "DimSecurityClassId": None,
            "DimMarketId": None,
            "DimInstrumentId": None,
            "DimDate": now,
            "DimTimeOfDay": now.time(),
            "DimSalesBookId": None,
            "Venue": "LSE",
            "IsCreated": "Y",
            "OrigQty": qty,
            "DeskDescription": "Main Desk",
            "SettlementRef": None,
            "ExecutionStrategy": None,
            "Owner": None,
            "Modifier": None,
            "DimModifierId": None,
            "DimOwnerId": None,
            "OrigLeavesQty": leaves_qty,
            "LastFilledSize": fill_qty,
            "LastFilledPrice": fill_price,
            "OrigExecAuthority": None,
            "PortfolioId": None,
            "ExecutionId": None,
            "ParValue": None,
            "TradableItems": None,
            "NumberOfTradableItems": None,
            "QuoteType": None,
            "SalesPerson": None,
            "EventSummary": None,
            "ClientName": None,
            "InternalCtpy": None,
            "InstrumentRef1": None,
            "InstrumentRef2": None,
            "InstrumentQuoteType": None,
            "SettlementDate": now,
            "Position": None,
            "Region": None,
            "FIorIRDFlag": None,
            "ClientNucleusID": None,
            "BankSide": None,
            "ProductDescription": None,
            "StellarOrderStatus": None,
            "StellarTransactionStatus": None,
            "StellarTransactionType": None,
            "BaseCcyLeavesQty": base_ccy_leaves_qty,
            "IsSpreadOrder": "N",
            "LinkedOrder": None,
            "OrdInstrumentType": None,
            "OrdExecType": None,
            "TrOrderStatus": None,
            "UnderlyingInstrumentCode": None,
            "ComponentId": None,
            "DimUnderlyingInstrumentId": None,
            "CancelCategory": None,
            "CFICode": None,
            "Origination": None,
            "QtyNotation": None
        }
        orders.append(order)
    return orders

def generate_trades(n=5):
    trades = []
    for i in range(n):
        now = datetime.datetime.now()
        qty = random.randint(1_000_000, 10_000_000)
        price = round(random.uniform(99, 101), 8)
        value = round(qty * price, 8)

        trade = {
            "SeqNum": i,
            "TradeEventId": i + 1000,
            "TradeFeedId": "TF1",
            "TradeFeedCounter": str(i),
            "TradeId": f"T{i}",
            "TradeAltId": f"TA{i}",
            "EventType": random.choice(["TN", "TR"]),
            "AgreedTime": now,
            "ReceivedTime": now,
            "TradeType": "Spot",
            "TradeSubType": "Normal",
            "SecurityClass": "SC1",
            "Symbol": "XYZ",
            "SymbolType": "Ticker",
            "SymbolDescription": "Synthetic Instrument",
            "InstrumentCode": "XYZ",
            "MarketId": "LSE",
            "Qty": qty,
            "CumulativeQty": qty,
            "LeavesQty": 0,
            "ReceivedPrice": price,
            "Price": price,
            "Currency": "EUR",
            "SettlementCurrency": "USD",
            "Side": random.choice(["B", "S"]),
            "ExecutionType": "Auto",
            "MaturityDate": now.date(),
            "StrikePrice": None,
            "PutCall": None,
            "BuyOrderId": f"O{i}",
            "BuyPartyId": f"Party{i}",
            "BuyPartyType": "Institution",
            "BuyDesk": "Desk1",
            "BuyDeskType": "Sales",
            "BuyTrader": f"Trader{i}",
            "SellOrderId": f"O{i+1}",
            "SellPartyId": f"Party{i+1}",
            "SellPartyType": "Institution",
            "SellDesk": "Desk2",
            "SellDeskType": "Trading",
            "SellTrader": f"Trader{i+1}",
            "TradeTime1": now,
            "TradeTime2": now,
            "TradeTime3": now,
            "TradeAttrib1": None,
            "TradeAttrib2": None,
            "TradeAttrib3": None,
            "TradeAttrib4": None,
            "TradeAttrib5": None,
            "TradeAttrib6": None,
            "TradeAttrib7": None,
            "Comments": None,
            "PrevTradeId": None,
            "IsCancelled": "N",
            "CancelTime": None,
            "IsAmended": "N",
            "AmendTime": None,
            "IsMonitored": "Y",
            "DataQualComment": None,
            "ReceivedValue": value,
            "Value": value,
            "BaseCcyValue": value,
            "Consideration": value,
            "BaseCcyConsideration": value,
            "MarkUp": None,
            "BaseCcyMarkUp": None,
            "DimMarketId": None,
            "DimInstrumentId": None,
            "DimBuyPartyId": None,
            "DimBuyDeskId": None,
            "DimSellPartyId": None,
            "DimSellDeskId": None,
            "DimAgreedDate": now,
            "DimAgreedTimeOfDay": now.time(),
            "DimReceivedDate": now,
            "DimReceivedTimeOfDay": now.time(),
            "DimDate1": now,
            "DimTimeOfDay1": now.time(),
            "DimDate2": now,
            "DimTimeOfDay2": now.time(),
            "DimDate3": now,
            "DimTimeOfDay3": now.time(),
            "DimBuyTraderId": None,
            "DimSellTraderId": None,
            "TradeAttrib8": None,
            "clr_code": None,
            "solicited": None,
            "ProductName": "Synthetic Product",
            "ProductDescription": "Synthetic Description",
            "ReferenceEntity": None,
            "RedCode": None,
            "TraderComment": None,
            "StartDate": now,
            "DealReference": None,
            "SecTransId": None,
            "InterestRateType": None,
            "InterestRate": None,
            "Spread": None,
            "RefRate": None,
            "LinkageReason": None,
            "LinkedTradeId": None,
            "Location": None,
            "BookOwner": None,
            "DimBookOwnerId": None,
            "IsTraderValid": True,
            "BrokerID": None,
            "Broker": None,
            "IsOvernightDeal": False,
            "DataDate": now.date(),
            "StandardSpread": None,
            "BorrowerCIS": None,
            "RepFrequency": None,
            "ProductState": None,
            "DealType": None,
            "FacilityRid": None,
            "FacilityName": None,
            "LoanEffectiveDate": now,
            "AssetClass": "FX",
            "EventDetails": None,
            "FacilityTypeDescription": None,
            "DiscountPremiumCurrency": None,
            "BuySellPct": None,
            "DealName": "Synthetic Deal",
            "Yield": round(random.uniform(0.01, 0.1), 8),
            "LegalEntity": "Synthetic Entity",
            "RepoRate": None,
            "Source": "Synthetic",
            "Venue": "LSE",
            "ECNReference": None,
            "SettlementDate": now.date(),
            "IsMateriallyAmended": False
        }
        trades.append(trade)
    return trades

def generate_market_depth(n=5):
    depth = []
    for i in range(n):
        now = datetime.datetime.now()
        side = random.choice(["Buy", "Sell"])
        price = round(100.0 + (0.01 * i if side == "Buy" else -0.01 * i), 7)
        quantity = random.randint(1_000_000, 5_000_000)
        base_ccy_quantity = float(quantity)

        entry = {
            "MarketDepthId": i,
            "DimInstrumentId": 100 + i,
            "VenueId": 1,
            "MarketTimestamp": now,
            "BookLevel": i + 1,
            "Side": side,
            "Price": price,
            "Quantity": quantity,
            "ReceivedTime": now,
            "FeedId": "MD1",
            "BaseCcyQuantity": base_ccy_quantity
        }
        depth.append(entry)
    return depth

# Example usage
orders = generate_orders(5)
trades = generate_trades(5)
market_depth = generate_market_depth(5)

# Convert to DataFrames for preview
orders_df = pd.DataFrame(orders)
trades_df = pd.DataFrame(trades)
depth_df = pd.DataFrame(market_depth)

print("Orders Sample:")
print(orders_df.head())

print("\nTrades Sample:")
print(trades_df.head())

print("\nMarket Depth Sample:")
print(depth_df.head())

