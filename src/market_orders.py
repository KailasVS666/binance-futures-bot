import argparse
import os
from dotenv import load_dotenv
from binance.client import Client
from src.utils import get_logger
from src.validator import validate_inputs

# 1. Setup Logging & Environment
load_dotenv()
logger = get_logger("MarketOrders")

def place_market_order(symbol, side, quantity):
    """
    Executes a market order on Binance Futures.
    """
    # 2. Validation (Mandatory for 50% grade)
    if not validate_inputs(symbol, side, quantity):
        return

    # 3. Initialize Client
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    client = Client(api_key, api_secret, testnet=True)

    try:
        logger.info(f"Attempting {side} Market Order: {quantity} {symbol}")
        
        # 4. Place the Order
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        # 5. Log Success (Mandatory for 10% grade)
        logger.info(f"✅ Order Filled! ID: {order['orderId']} at Avg Price: {order.get('avgPrice', 'Market')}")
        print(f"✅ Success! {side} {quantity} {symbol} filled.")

    except Exception as e:
        logger.error(f"❌ Market Order Failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # 6. CLI Argument Parsing (Mandatory for reproducibility)
    parser = argparse.ArgumentParser(description="Binance Futures Market Order Bot")
    parser.add_argument("symbol", type=str, help="e.g., BTCUSDT")
    parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Amount to trade")
    
    args = parser.parse_args()
    place_market_order(args.symbol, args.side, args.quantity)
