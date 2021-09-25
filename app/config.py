import os
import datetime as dt

LOGGING_LEVEL = 'DEBUG'

TOKEN = '1907978319:AAF9ObvJwFekyuFQwuJJTCsS64VI9NTR9Dg'

SPBU_TT_API_REQUEST_TIMEOUT = os.environ['SPBU_TT_API_REQUEST_TIMEOUT']

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
DB_SCHEMA = os.environ['DB_SCHEMA']
DB_HOST = os.environ['DB_HOST']
DB_MIGRATIONS_TABLE = 'migrations'

ADMIN_PASS = os.environ['ADMIN_PASS']

TIME_ZONE = os.environ.get('TIME_ZONE', '3')
SCHEDULER_TIME = os.environ.get('SCHEDULER_TIME', '02:19')
