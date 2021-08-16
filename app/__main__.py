import app.bot.timetable_bot as bot
import app.repository.migrations.migration_manager as migrations

migrations.execute_migrations()
bot.start()

