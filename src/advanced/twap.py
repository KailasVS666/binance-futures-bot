import os
import time
import argparse
from dotenv import load_dotenv
from binance.client import Client
from src.utils import get_logger

# 1. Load environment variables (Mandatory for security)
load_dotenv()
logger = get_logger("TWAP")

def execute_twap(symbol, side, total_quantity, chunks, interval_seconds):
    """
    Executes a TWAP strategy by splitting an order into smaller parts.
    """
    client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'), testnet=True)
    
    # Sync timestamp (Requirement for reliability)
    server_time = client.get_server_time()
    client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
    
    chunk_size = round(total_quantity / chunks, 3)
    logger.info(f"Starting TWAP: {total_quantity} {symbol} split into {chunks} chunks.")

    for i in range(chunks):
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=chunk_size
            )
            logger.info(f"✅ Chunk {i+1}/{chunks} filled: {chunk_size} {symbol}")
            print(f"✅ Successfully filled chunk {i+1} of {chunks}")
            
            if i < chunks - 1:
                time.sleep(interval_seconds)
                
        except Exception as e:
            logger.error(f"❌ TWAP Error at chunk {i+1}: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("total_qty", type=float)
    parser.add_argument("chunks", type=int)
    parser.add_argument("interval", type=int)
    args = parser.parse_args()
    
    execute_twap(args.symbol, args.side, args.total_qty, args.chunks, args.interval)
