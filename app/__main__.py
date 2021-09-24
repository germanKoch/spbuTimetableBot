import logging
import threading

import app.bot.timetable_bot as bot
import app.repository.migrations.migration_manager as migrations
import app.botscheduler.bot_scheduler as scheduler
from app.logger_configurer import config_logger

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
