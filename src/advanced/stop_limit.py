import argparse
import os
from dotenv import load_dotenv
from binance.client import Client
from src.utils import get_logger
from src.validator import validate_inputs

load_dotenv()
logger = get_logger("StopLimit")

def place_stop_limit(symbol, side, quantity, price, stop_price):
    if not validate_inputs(symbol, side, quantity, price):
        return

    client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'), testnet=True)

    try:
        logger.info(f"Setting {side} Stop-Limit: {quantity} {symbol} (Trigger: {stop_price}, Limit: {price})")
        
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='STOP',
            timeInForce='GTC',
            quantity=quantity,
            price=price,
            stopPrice=stop_price
        )
        
        # Check for either 'orderId' (standard) or 'algoId' (conditional)
        order_id = order.get('orderId') or order.get('algoId')
        
        if order_id:
            logger.info(f"✅ Stop-Limit Active! ID: {order_id}")
            print(f"✅ Success! {side} Stop-Limit set. ID: {order_id}")
        else:
            logger.error(f"❌ Unexpected Response: {order}")
            print(f"❌ Failed. Binance Response: {order}")

    except Exception as e:
        logger.error(f"❌ API Error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("price", type=float)
    parser.add_argument("stop_price", type=float)
    
    args = parser.parse_args()
    place_stop_limit(args.symbol, args.side, args.quantity, args.price, args.stop_price)
