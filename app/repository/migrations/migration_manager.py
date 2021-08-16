import app.config as config
import app.repository.migrations.migrations as steps
import re

from inspect import getmembers, isfunction
from typing import List
from app.repository.connection import update_query
from app.repository.connection import get_row_query
from app.repository.connection import update_queries


class Migration:
    id: int
    version: int
    is_executed: bool

    def __init__(self, id, version, is_executed):
        self.id = id
        self.version = version
        self.is_executed = is_executed

    def __repr__(self):
        return f"Migration({self.id}, {self.version}, {self.is_executed})"


def map_migration(row) -> Migration:
    return Migration(id=row["id"], version=row["version"], is_executed=row["is_executed"])


def filter_script(script, last_v):
    groups = re.search('version_(\d)', script[0]).groups()
    if len(groups) > 0:
        return int(groups[0]) > last_v
    return False


def execute_migrations():
    query = f'CREATE TABLE IF NOT EXISTS {config.DB_MIGRATIONS_TABLE} (id serial, version integer, is_executed boolean)'
    update_query(query)

    query = f'SELECT * FROM {config.DB_MIGRATIONS_TABLE} WHERE is_executed=true ORDER BY version DESC '
    migrations = list(map(map_migration, get_row_query(query)))
    last_version = 0
    if len(migrations) != 0:
        last_version = migrations[0].version

    scripts = list(filter(lambda fun: filter_script(last_v=last_version, script=fun), getmembers(steps, isfunction)))
    scripts.sort(key=lambda fun: fun[0])

    queries: List[str] = []
    for index, script in enumerate(scripts):
        query = script[1]()
        version = last_version + index + 1
        add_migration_query = f'INSERT INTO {config.DB_MIGRATIONS_TABLE}(version, is_executed) VALUES ({version}, true)'
        queries.append(query)
        queries.append(add_migration_query)
    update_queries(queries)
