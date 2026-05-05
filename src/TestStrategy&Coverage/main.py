from pricing.calculator import calculate_price
from decimal import Decimal
from datetime import datetime

if __name__ == "__main__":
    # Esempi di chiamata
    examples = [
        {"base_price": 50, "coupon_code": "save10", "quantity": 2, "user_status": "regular"},
        {"base_price": "120.00", "coupon_code": "save20", "quantity": 1, "user_status": "vip"},
        {"base_price": 30, "coupon_code": "bogo", "quantity": 3, "user_status": "staff"},
        {"base_price": 10, "coupon_code": None, "quantity": 5, "user_status": "regular", "purchased_at": datetime(2026, 3, 2, 19, 0)},
    ]
    for i, params in enumerate(examples, 1):
        try:
            result = calculate_price(**params)
            print(f"Esempio {i}: prezzo finale = {result}")
        except Exception as e:
            print(f"Esempio {i}: errore: {e}")
