import os
from dotenv import load_dotenv
from binance.client import Client

# Load keys from the .env file
load_dotenv()
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Initialize the client for TESTNET (Demo)
client = Client(api_key, api_secret, testnet=True)

try:
    # Fetch account information to verify connection
    info = client.futures_account()
    print("✅ Connection Successful!")
    print(f"Total Wallet Balance: {info['totalWalletBalance']} USDT")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
