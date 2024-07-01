from datetime import datetime, timedelta, timezone
import timeago

def format_time_ago(date: datetime):
    date = date.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return timeago.format(date,now)
