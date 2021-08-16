from app.domain.subs_types import *
from app.repository.connection import get_row_query
from app.repository.connection import update_query
from app.repository.connection import update_queries
from app.domain.exception.not_found_exception import NotFoundException

table = "subscription"


def map_subs(row) -> Subscription:
    return Subscription(
        chat_id=row["chat_id"],
        state=row["state"],
        division_alias=row["division_alias"],
        level=row["level"],
        program=row["program"],
        year=row["year"],
        program_id=row["program_id"],
        group_id=row["group_id"]
    )


def get_by_chat_id(chat_id: int) -> Subscription:
    query = f"SELECT * FROM {table} WHERE chat_id = %(chat_id)s"
    params = {'chat_id': chat_id}
    subs = list(map(map_subs, get_row_query(query, params)))
    if len(subs) == 0:
        raise NotFoundException("subs not found")
    return subs[0]


def create_subs(chat_id: int, state: str):
    delete_query = f"DELETE FROM {table} WHERE chat_id={chat_id}"
    create_query = f"INSERT INTO {table}(chat_id, state) VALUES ({chat_id}, {state})"
    update_queries([delete_query, create_query])


def update_subs(chat_id: int, params: dict):
    query = f"UPDATE {table} SET"
    query_params = {}
    for key, value in params.items():
        query += f" {key}=%({key})s,"
        query_params[key] = value
    query = query[:-1]
    query += f" WHERE chat_id=%(chat_id)s"
    query_params["chat_id"] = chat_id
    update_query(query, query_params)
