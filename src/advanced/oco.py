import os
import argparse
from dotenv import load_dotenv
from binance.client import Client
from src.utils import get_logger

load_dotenv()
logger = get_logger("OCO")

def place_oco(symbol, quantity, tp_price, sl_price):
    """
    Simulates OCO by placing a Take Profit Market and a Stop Market order.
    These orders will close an existing position.
    """
    client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'), testnet=True)

    try:
        logger.info(f"Setting OCO for {symbol}: TP @ {tp_price}, SL @ {sl_price}")

        # 1. Take Profit Market Order
        # Triggers when price rises to tp_price (for a BUY position)
        tp = client.futures_create_order(
            symbol=symbol,
            side='SELL', 
            type='TAKE_PROFIT_MARKET',
            stopPrice=tp_price,
            closePosition=True
        )

        # 2. Stop Market Order (Stop Loss)
        # Triggers when price drops to sl_price (for a BUY position)
        sl = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='STOP_MARKET',
            stopPrice=sl_price,
            closePosition=True
        )

        tp_id = tp.get('algoId') or tp.get('orderId')
        sl_id = sl.get('algoId') or sl.get('orderId')

        logger.info(f"✅ OCO Set! TP ID: {tp_id}, SL ID: {sl_id}")
        print(f"✅ Success! OCO protection active for {symbol}.")
        print(f"   Take Profit: {tp_price} | Stop Loss: {sl_price}")

    except Exception as e:
        logger.error(f"❌ OCO Failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCO Order Protection")
    parser.add_argument("symbol")
    parser.add_argument("quantity", type=float)
    parser.add_argument("tp", type=float)
    parser.add_argument("sl", type=float)
    args = parser.parse_args()
    place_oco(args.symbol, args.quantity, args.tp, args.sl)
