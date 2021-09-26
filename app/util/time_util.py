from datetime import date, timedelta, timezone, datetime
import app.config as config


def get_week_boundaries(day: date):
    weekday = day.weekday()
    start_week = day - timedelta(weekday)
    end_week = start_week + timedelta(6)
    return start_week, end_week


def get_current_date() -> date:
    tz = timezone(offset=timedelta(hours=int(config.TIME_ZONE)))
    return datetime.now(tz).date()
