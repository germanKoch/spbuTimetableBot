import time

import schedule

import app.bot.timetable_bot as bot
import app.config as config


def start():
    schedule.every().day.at(config.SCHEDULER_TIME).do(bot.send_day_events)

    while True:
        schedule.run_pending()
        time.sleep(1)
