from src.utils import get_logger

logger = get_logger("Validator")

def validate_inputs(symbol, side, quantity, price=None):
    """
    Validates trading parameters to prevent API errors.
    """
    try:
        if not symbol.endswith("USDT"):
            raise ValueError(f"Invalid symbol '{symbol}'. Must end with 'USDT'.")
        
        if side not in ["BUY", "SELL"]:
            raise ValueError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'.")
        
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
            
        if price is not None and price <= 0:
            raise ValueError("Price must be greater than zero for limit orders.")
            
        return True
    except Exception as e:
        logger.error(f"Validation Failed: {e}")
        return False
