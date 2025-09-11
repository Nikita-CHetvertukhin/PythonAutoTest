from datetime import datetime, timedelta
from tzlocal import get_localzone
import uuid

def get_date(day_label):
    today = datetime.now()
    delta = {
        'today': 0,
        'tomorrow': 1,
        'yesterday': -1
    }.get(day_label.lower(), 0)
    
    target_date = today + timedelta(days=delta)
    return target_date.strftime('%d.%m.%Y')

def get_timestamp():
    """Возвращает текущую дату и время в формате YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_uuid(length: int = 5) -> str:
    """
    Возвращает уникальный идентификатор — первые `length` символов UUID4.
    """
    return uuid.uuid4().hex[:length]

def get_timezone_info():
    now = datetime.now(get_localzone())
    offset = now.strftime('%z')  # Пример: +0200
    return offset