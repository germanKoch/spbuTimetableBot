import datetime as dt
import time

import schedule

import app.bot.timetable_bot as bot
import app.config as config


def start():
    zone_offset = -int(time.timezone.real/3600) - int(config.TIME_ZONE)
    schedule_time_without_offset = dt.time.fromisoformat(config.SCHEDULER_TIME)
    schedule_time = dt.time(hour=(schedule_time_without_offset.hour + zone_offset) % 24,
                            minute=schedule_time_without_offset.minute)
    schedule.every().day.at(schedule_time.isoformat()).do(bot.send_day_events)
    while True:
        schedule.run_pending()
        time.sleep(1)
