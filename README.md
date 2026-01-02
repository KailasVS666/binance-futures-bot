# Binance Futures Trading Bot - ICU Guardian (BoltDev)

## Project Overview
A professional Python-based automated trading system for Binance Futures. This bot handles basic and advanced order types with integrated security, robust input validation, and server-time synchronization.

## Core Features
- **Security**: Utilizes `.env` for secure API key management.
- **Validation**: Strict checks for trade quantities, prices, and symbols.
- **Reliability**: Automatic timestamp synchronization to prevent -1021 synchronization errors.
- **Advanced Logic**: Simulated OCO (One-Cancels-the-Other) protection using conditional orders.

## Installation
1. Ensure Python 3.10+ is installed.
2. Create a virtual environment: `python -m venv venv`.
3. Activate the environment: `.\venv\Scripts\Activate.ps1`.
4. Install requirements: `pip install python-binance python-dotenv`.

## Usage Guide
Always run scripts from the project root using the module flag (`-m`).

| Feature | Command |
| :--- | :--- |
| **Connection Test** | `python src/test_connection.py` |
| **Market Order** | `python -m src.market_orders BTCUSDT BUY 0.003` |
| **Limit Order** | `python -m src.limit_orders BTCUSDT BUY 0.003 85000` |
| **Stop-Limit** | `python -m src.advanced.stop_limit BTCUSDT BUY 0.003 90100 90000` |
| **OCO Protection** | `python -m src.advanced.oco BTCUSDT 0.003 95000 85000` |

## Technical Implementation Notes
- **Error Handling**: The bot specifically handles Binance API errors like `4016` (Price Filter) and `4130` (Order Conflict).
- **Time Sync**: Every script pings the Binance server to calculate a `timestamp_offset`, ensuring local clock drift does not cause request rejections.