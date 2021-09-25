import datetime as dt

import app.config as config
import app.service.subs.subs_service as subs_service
import app.service.timetable.timetable_service as spbu_service
from app.domain.response import Response
from app.domain.subs_types import *
from app.domain.timetable_types import *
from app.util.week_util import get_week_boundaries


def get_day_events(chat_id) -> Response:
    subs = subs_service.get_by_chat_id(chat_id)
    day = _get_day_events(_get_current_date(), subs.group_id)
    text = _get_text(day)
    return Response(text=text, buttons=[])


def get_day_events_all(callback):
    subs = subs_service.get_all()
    subs = list(filter(lambda sub: sub.state == STATE.SAVED_GROUP and sub.is_active, subs))
    for sub in subs:
        day = _get_day_events(_get_current_date(), sub.group_id)
        text = _get_text(day)
        callback(sub.chat_id, text)


def _get_day_events(current_date, group_id) -> Day:
    from_date, to_date = get_week_boundaries(current_date)
    days = spbu_service.get_events(group_id, from_date, to_date)
    return next((day for day in days if day.day_date == current_date), None)


def _get_current_date() -> date:
    timezone = dt.timezone(offset=dt.timedelta(hours=int(config.TIME_ZONE)))
    return dt.datetime.now(timezone).date()


def _get_text(day: Day) -> str:
    if day is not None and len(day.events) > 0:
        return _map_day(day)
    else:
        return f'Кажется, пар нету. Можно отдохнуть)'


def _map_day(day: Day) -> str:
    representation = str()
    representation += '\n\n' + day.day_string + '\n\n'
    for event in day.events:
        representation += "Предмет: " + event.subject + "\n"
        representation += "Преподаватели: " + event.educators + "\n"
        representation += "Начало: " + event.start_datetime.time().isoformat()
        representation += ", Конец: " + event.end_datetime.time().isoformat()
        representation += "\n\n"
    return representation
