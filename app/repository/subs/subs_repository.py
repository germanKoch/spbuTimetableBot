from app.domain.exception.not_found_exception import NotFoundException
from app.repository.connection import get_row_query
from app.repository.connection import update_query

table = "subscription"


def get_all() -> dict:
    query = f"SELECT * FROM {table}"
    return get_row_query(query)


def get_by_chat_id(chat_id: int) -> dict:
    query = f"SELECT * FROM {table} WHERE chat_id = %(chat_id)s"
    params = {'chat_id': chat_id}
    subs = get_row_query(query, params)
    if len(subs) == 0:
        raise NotFoundException("subs not found")
    return subs[0]


def create_subs(params: dict):
    delete_query = f"DELETE FROM {table} WHERE chat_id={params['chat_id']}"
    keys = ", ".join(params.keys())
    values = ", ".join(map(lambda key: f"%({key})s", params.keys()))
    create_query = f"INSERT INTO {table}({keys}) VALUES ({values})"
    update_query(delete_query)
    update_query(create_query, params)


def update_subs(params: dict):
    query = f"UPDATE {table} SET"
    query_params = {}
    for key, value in params.items():
        query += f" {key}=%({key})s,"
        query_params[key] = value
    query = query[:-1]
    query += f" WHERE chat_id=%(chat_id)s"
    query_params["chat_id"] = params['chat_id']
    update_query(query, query_params)
