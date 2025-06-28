from datetime import datetime, timedelta

def get_date(day_label):
    today = datetime.now()
    delta = {
        'today': 0,
        'tomorrow': 1,
        'yesterday': -1
    }.get(day_label.lower(), 0)
    
    target_date = today + timedelta(days=delta)
    return target_date.strftime('%d.%m.%Y')