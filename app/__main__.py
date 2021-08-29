from urllib3.exceptions import ReadTimeoutError
import app.bot.timetable_bot as bot
import app.scheduler.scheduler as scheduler
import app.repository.migrations.migration_manager as migrations

try:
    migrations.execute_migrations()
    scheduler.start()
    bot.start()
except ReadTimeoutError:
    print("ReadTimeoutError")
