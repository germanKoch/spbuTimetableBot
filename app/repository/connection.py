from contextlib import closing
from typing import List

import psycopg2
from psycopg2.extras import DictCursor

import app.config as config


def get_conn():
    return psycopg2.connect(
        cursor_factory=DictCursor,
        dbname=f"{config.DB_NAME}",
        user=f"{config.DB_USER}",
        password=f"{config.DB_PASSWORD}",
        host=f"{config.DB_HOST}",
        port=f"{config.DB_PORT}",
        options=f"-c search_path={config.DB_SCHEMA}"
    )


def get_row_query(query, parameters=None):
    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()


def update_query(query, parameters=None):
    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            conn.commit()


def update_queries(queries: List[str]):
    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
            conn.commit()
