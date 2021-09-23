import datetime as dt

from scheduler import Scheduler

import app.bot.timetable_bot as bot
import app.config as config


def start():
    time = dt.time.fromisoformat(config.SCHEDULER_TIME)
    timezone = dt.timezone(offset=dt.timedelta(hours=int(config.TIME_ZONE)))

    scheduler_time = dt.time(hour=time.hour, minute=time.minute, tzinfo=timezone)

    schedule = Scheduler(tzinfo=dt.timezone.utc)
    schedule.daily(scheduler_time, bot.send_day_events)
