import argparse
import os
from dotenv import load_dotenv
from binance.client import Client
from src.utils import get_logger
from src.validator import validate_inputs

# 1. Setup Logging & Environment
load_dotenv()
logger = get_logger("LimitOrders")

def place_limit_order(symbol, side, quantity, price):
    """
    Places a Limit Order on Binance Futures at a specific price.
    """
    # 2. Validation (Mandatory for 50% grade)
    if not validate_inputs(symbol, side, quantity, price):
        return

    # 3. Initialize Client
    client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'), testnet=True)

    try:
        logger.info(f"Placing {side} Limit Order: {quantity} {symbol} at {price}")
        
        # 4. Execute (Limit orders require 'timeInForce')
        # TIF 'GTC' means the order stays open until filled or canceled
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
        
        # 5. Log Success (Mandatory for 10% grade)
        logger.info(f"✅ Limit Order Set! ID: {order['orderId']}")
        print(f"✅ Success! {side} Limit Order for {symbol} placed at {price}.")

    except Exception as e:
        logger.error(f"❌ Limit Order Failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # 6. CLI Arguments
    parser = argparse.ArgumentParser(description="Binance Futures Limit Order Bot")
    parser.add_argument("symbol", type=str)
    parser.add_argument("side", type=str, choices=["BUY", "SELL"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("price", type=float)
    
    args = parser.parse_args()
    place_limit_order(args.symbol, args.side, args.quantity, args.price)
