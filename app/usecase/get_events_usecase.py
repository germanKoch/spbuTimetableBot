import app.service.subs.subs_service as subs_service
import app.service.timetable.timetable_service as spbu_service
from app.domain.subs_types import *
from app.domain.timetable_types import *
from app.util.week_util import get_week_boundaries


def get_day_events(chat_id, current_date) -> Day:
    subs = subs_service.get_by_chat_id(chat_id)
    return _get_day_events(current_date, subs.group_id)


def get_day_events_all(current_date: date, callback):
    subs = subs_service.get_all()
    subs = list(filter(lambda sub: sub.state == STATE.SAVED_GROUP, subs))
    for sub in subs:
        events = _get_day_events(current_date, sub.group_id)
        callback(sub.chat_id, events)


def _get_day_events(current_date, group_id):
    from_date, to_date = get_week_boundaries(current_date)
    days = spbu_service.get_events(group_id, from_date, to_date)
    return next((day for day in days if day.day_date == current_date), None)
