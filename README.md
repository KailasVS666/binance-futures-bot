# Binance Futures Trading Bot

A Python CLI trading bot for Binance Futures that supports market, limit, stop-limit, OCO-style protection, and TWAP execution workflows on testnet.

## Overview

This project is structured as a set of focused command-line modules. Each module performs one trading action, logs to both console and file, and uses Binance Futures endpoints through `python-binance`.

The bot is intended for educational, practice, and workflow-automation purposes. All order modules currently initialize the client with `testnet=True`.

## What This Project Includes

- Market order execution for immediate entry/exit
- Limit order placement with `GTC` time-in-force
- Stop-limit style order placement with trigger and limit prices
- OCO-like protection using paired futures conditional close orders
- TWAP execution by splitting a large order into timed chunks
- Connection test script for credentials and account access checks
- Shared structured logging (`bot.log`) and input validation helpers

## Architecture

```text
src/
	__init__.py
	utils.py              -> logger factory (file + console handlers)
	validator.py          -> symbol/side/quantity/price checks
	test_connection.py    -> API connectivity and wallet balance check
	market_orders.py      -> futures market orders
	limit_orders.py       -> futures limit orders (GTC)
	advanced/
		stop_limit.py       -> stop-triggered limit order flow
		oco.py              -> take-profit + stop-loss protection pair
		twap.py             -> chunked market execution over time
```

## Detailed Module Description

### `src/utils.py`
- Provides `get_logger(module_name)`.
- Creates consistent log format with timestamp, logger name, level, and message.
- Writes logs to both terminal and `bot.log`.
- Prevents duplicate handlers when logger is reused.

### `src/validator.py`
- Provides `validate_inputs(symbol, side, quantity, price=None)`.
- Enforces:
	- Symbol must end with `USDT`
	- Side must be `BUY` or `SELL`
	- Quantity must be greater than zero
	- Price (when provided) must be greater than zero
- Returns `True`/`False` and logs validation failures.

### `src/test_connection.py`
- Loads API credentials from `.env`.
- Connects to Binance Futures testnet.
- Calls `futures_account()` and prints wallet balance.
- Useful as first diagnostic step before placing orders.

### `src/market_orders.py`
- Implements `place_market_order(symbol, side, quantity)`.
- Validates inputs using `validator.py`.
- Synchronizes timestamp offset using Binance server time.
- Places `MARKET` futures order and logs result.

### `src/limit_orders.py`
- Implements `place_limit_order(symbol, side, quantity, price)`.
- Validates inputs including price.
- Synchronizes timestamp offset.
- Places `LIMIT` futures order with `timeInForce='GTC'`.

### `src/advanced/stop_limit.py`
- Implements `place_stop_limit(symbol, side, quantity, price, stop_price)`.
- Validates base inputs via `validator.py`.
- Synchronizes timestamp offset.
- Places conditional stop-limit flow using `type='STOP'`, `stopPrice`, and limit `price`.

### `src/advanced/oco.py`
- Implements `place_oco(symbol, quantity, tp_price, sl_price)`.
- Synchronizes timestamp offset.
- Places two futures conditional close orders:
	- `TAKE_PROFIT_MARKET` with `closePosition=True`
	- `STOP_MARKET` with `closePosition=True`
- Logs both resulting order IDs.

### `src/advanced/twap.py`
- Implements `execute_twap(symbol, side, total_quantity, chunks, interval_seconds)`.
- Synchronizes timestamp offset.
- Splits total quantity into equal chunks.
- Executes chunked `MARKET` orders with sleep intervals.

## Setup

### 1) Requirements
- Python 3.10+
- Binance Futures API key/secret
- Packages:
	- `python-binance`
	- `python-dotenv`

### 2) Environment Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install python-binance python-dotenv
```

### 3) Create `.env`

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

## Usage

Run commands from the project root.

### Connection Test

```powershell
python src/test_connection.py
```

### Market Order

```powershell
python -m src.market_orders BTCUSDT BUY 0.003
```

Arguments:
- `symbol`: trading pair like `BTCUSDT`
- `side`: `BUY` or `SELL`
- `quantity`: positive float

### Limit Order

```powershell
python -m src.limit_orders BTCUSDT BUY 0.003 85000
```

Arguments:
- `symbol`
- `side`
- `quantity`
- `price`: limit price

### Stop-Limit Order

```powershell
python -m src.advanced.stop_limit BTCUSDT BUY 0.003 90100 90000
```

Arguments:
- `symbol`
- `side`
- `quantity`
- `price`: limit execution price
- `stop_price`: trigger price

### OCO-Style Protection

```powershell
python -m src.advanced.oco BTCUSDT 0.003 95000 85000
```

Arguments:
- `symbol`
- `quantity`
- `tp`: take-profit trigger price
- `sl`: stop-loss trigger price

### TWAP Execution

```powershell
python -m src.advanced.twap BTCUSDT BUY 0.300 3 5
```

Arguments:
- `symbol`
- `side`
- `total_qty`: full quantity to execute
- `chunks`: number of child orders
- `interval`: delay (seconds) between chunks

## Logging and Observability

- Logs are written to terminal and `bot.log`.
- Format:

```text
timestamp - module_name - level - message
```

- This makes it easier to audit order attempts and failures.

## Operational Notes

- Credentials are loaded from `.env` using `python-dotenv`.
- Order modules synchronize local timestamp offset with Binance server time to reduce request timestamp issues.
- Validation is enforced in core order modules before API execution.

## Assignment Context (Short)

This repository also reflects an assignment-style implementation focus: input validation, structured logging, reproducible CLI usage, and robust timestamp handling across order scripts.

## Future Improvements

- Add `requirements.txt` for repeatable dependency installs.
- Add `.env.example` for faster onboarding.
- Centralize Binance client and time-sync logic to remove duplication.
- Add unified validation for advanced modules (OCO/TWAP-specific checks).
- Add richer order-state tracking (submitted/open/filled/canceled).
- Add optional mainnet toggle with explicit safety guardrails.

## Disclaimer

This software is for education and experimentation. Trading involves risk. Test thoroughly and apply strict risk controls before considering any production or live-trading usage.