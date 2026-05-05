from datetime import datetime
from typing import Optional

def get_effective_purchase_datetime(purchased_at: Optional[datetime]) -> datetime:
    return purchased_at if purchased_at is not None else datetime.utcnow()

def is_time_sale(dt: datetime) -> bool:
    return 18 <= dt.hour <= 23