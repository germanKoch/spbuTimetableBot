from app.domain.subs_types import *
import app.repository.subs.subs_repository as repository


def get_by_chat_id(chat_id: int) -> Subscription:
    return repository.get_by_chat_id(chat_id)


def create_subs(chat_id: int):
    repository.update_subs(chat_id, {
        'state': STATE.START
    })


def set_division(chat_id: int, division_alias: str):
    repository.update_subs(chat_id, {
        'state': STATE.SAVED_DIVISION,
        'division_alias': division_alias
    })


def set_level(chat_id: int, level: str):
    repository.update_subs(chat_id, {
        'state': STATE.SAVED_LEVEL,
        'level': level
    })


def set_program(chat_id: int, program: str):
    repository.update_subs(chat_id, {
        'state': STATE.SAVED_PROGRAM,
        'program': program
    })


def set_year(chat_id: int, year: str):
    repository.update_subs(chat_id, {
        'state': STATE.SAVED_YEAR,
        'year': year
    })


def set_program_id(chat_id: int, program_id: str):
    repository.update_subs(chat_id, {
        'state': STATE.SAVED_PROGRAM_ID,
        'program_id': program_id
    })


def set_group_id(chat_id: int, group_id: int):
    repository.update_subs(chat_id, {
        'state': STATE.SAVED_GROUP,
        'group_id': group_id,
    })
