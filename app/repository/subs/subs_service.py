from typing import List
from app.repository.subs.subs_types import *

subs_dict = dict()


def get_by_id(chat_id: str) -> Subscription:
    return subs_dict[chat_id]


def create_subs(chat_id: str):
    subs = Subscription()
    subs.chat_id = chat_id
    subs.state = STATE.START
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_division(chat_id: str, division_alias: str):
    subs = subs_dict[chat_id]
    subs.division_alias = division_alias
    subs.state = STATE.ENTER_DIVISION
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_level(chat_id: str, level: str):
    subs = subs_dict[chat_id]
    subs.level = level
    subs.state = STATE.ENTER_LEVEL
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_program(chat_id: str, program_id: str):
    subs = subs_dict[chat_id]
    subs.program = program_id
    subs.state = STATE.ENTER_PROGRAM
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_year(chat_id: str, year: str):
    subs = subs_dict[chat_id]
    subs.year = year
    subs.state = STATE.ENTER_YEAR
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_program_id(chat_id: str, program_id: str):
    subs = subs_dict[chat_id]
    subs.program_id = program_id
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_group_id(chat_id: str, group_id: int):
    subs = subs_dict[chat_id]
    subs.group_id = group_id
    subs.state = STATE.ENTER_GROUP
    subs_dict[chat_id] = subs
    print(subs_dict)


def set_complete(chat_id: str, group_id: int):
    subs = subs_dict[chat_id]
    subs.state = STATE.ENTER_GROUP
    subs_dict[chat_id] = subs
    print(subs_dict)


def get_state(chat_id: str):
    if chat_id in subs_dict:
        subs = subs_dict[chat_id]
        print(subs)
        return subs.state
    return None
