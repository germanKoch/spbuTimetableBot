from datetime import date, timedelta


def get_week_boundaries(day: date):
    weekday = day.weekday()
    start_week = day - timedelta(weekday)
    end_week = start_week + timedelta(6)
    return start_week, end_week
