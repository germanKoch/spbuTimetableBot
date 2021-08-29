import app.repository.subs.subs_repository as repository
from app.domain.subs_types import *


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


def get_all():
    rows = repository.get_all()
    return list(map(map_subs, rows))


def create_subs(subs: Subscription):
    subs_dict = vars(subs)
    repository.create_subs(subs_dict)


def get_by_chat_id(chat_id: int) -> Subscription:
    return map_subs(repository.get_by_chat_id(chat_id))


def update(subs: Subscription):
    subs_dict = vars(subs)
    repository.update_subs(subs_dict)
