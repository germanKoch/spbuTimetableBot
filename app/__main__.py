import threading

from urllib3.exceptions import ReadTimeoutError
from app.logger_configurer import config_logger
import logging

import app.bot.timetable_bot as bot
import app.repository.migrations.migration_manager as migrations
import app.scheduler.scheduler as scheduler

log = logging.getLogger(__name__)

try:
    config_logger()
    migrations.execute_migrations()
    scheduler_thread = threading.Thread(target=scheduler.start, args=[])
    bot_thread = threading.Thread(target=bot.start, args=[])
    scheduler_thread.start()
    bot_thread.start()
except Exception as e:
    log.exception(e)
