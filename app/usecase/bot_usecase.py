import app.service.subs.subs_service as subs_service
import app.service.timetable.timetable_service as spbu_service
from app.domain.exception.not_found_exception import NotFoundException
from app.domain.subs_types import *
from app.domain.timetable_types import *
from app.domain.response import Response
from app.util.week_util import get_week_boundaries


# TODO: добавить проверку стэйтов
def start(chat_id) -> Response:
    subs_service.create_subs(Subscription(chat_id=chat_id, state=STATE.START))
    text = f"Привет! Я бот расписаний. Выбери факультет"
    buttons = list(map(lambda division: division.name, spbu_service.get_divisions()))
    return Response(text, buttons)


def enter_division(chat_id, division_name) -> Response:
    try:
        division = spbu_service.get_division(division_name)
        levels = spbu_service.get_levels(division.alias)

        subs = subs_service.get_by_chat_id(chat_id)
        subs.division_alias = division.alias
        subs.state = STATE.SAVED_DIVISION
        subs_service.update(subs)

        buttons = list(map(lambda level: level.name, levels))
        text = "Выбери уровень: "
        return Response(text, buttons)
    except NotFoundException:
        text = "Упс. Кажется, я не смог найти такой факультет. Попробуй ещё раз."
        buttons = list(map(lambda division: division.name, spbu_service.get_divisions()))
        return Response(text, buttons)


def enter_level(chat_id, level_name) -> Response:
    subs = subs_service.get_by_chat_id(chat_id)
    try:
        level = spbu_service.get_level(subs.division_alias, level_name)
        subs.level = level.name
        subs.state = STATE.SAVED_LEVEL
        subs_service.update(subs)

        text = "Отлично! Теперь выбери программу обучения."
        buttons = list(map(lambda program: program.name, level.programs))
        return Response(text, buttons)
    except NotFoundException:
        text = "Упс. Кажется, я не смог найти такой уровень. Попробуй ещё раз."
        buttons = list(map(lambda level: level.name, spbu_service.get_levels(subs.division_alias)))
        return Response(text, buttons)


def enter_program(chat_id, program_name) -> Response:
    subs = subs_service.get_by_chat_id(chat_id)
    try:
        program = spbu_service.get_program(subs.division_alias, subs.level, program_name)
        subs.program = program.name
        subs.state = STATE.SAVED_PROGRAM
        subs_service.update(subs)

        text = "Отлично! Выбери год!"
        buttons = list(map(lambda admission: admission.year, program.admissions))
        return Response(text, buttons)
    except NotFoundException:
        level = spbu_service.get_level(subs.division_alias, subs.level)

        text = "Упс. Кажется, я не смог найти такую программу. Попробуй ещё раз."
        buttons = list(map(lambda program: program.name, level.programs))
        return Response(text, buttons)


def enter_year(chat_id, year) -> Response:
    subs = subs_service.get_by_chat_id(chat_id)
    try:
        admission = spbu_service.get_admission(subs.division_alias, subs.level, subs.program, year)
        groups = spbu_service.get_groups(admission.program_id)

        subs.year = admission.year
        subs.program_id = admission.program_id
        subs.state = STATE.SAVED_PROGRAM_ID
        subs_service.update(subs)

        text = "Отлично! Почти всё. Осталось выбрать группу."
        buttons = list(map(lambda group: group.name, groups))
        return Response(text, buttons)
    except NotFoundException:
        program = spbu_service.get_program(subs.division_alias, subs.level, subs.program)

        text = "Упс. Кажется, я не смог найти такой год. Попробуй ещё раз."
        buttons = list(map(lambda admission: admission.year, program.admissions))
        return Response(text, buttons)


def entering_group(chat_id, group_name) -> Response:
    subs = subs_service.get_by_chat_id(chat_id)
    try:
        group = spbu_service.get_group(subs.program_id, group_name)
        subs.group_id = group.id
        subs.state = STATE.SAVED_GROUP
        subs_service.update(subs)

        text = "Отлично! Зареган"
        buttons = list()
        return Response(text, buttons)
    except NotFoundException:
        groups = spbu_service.get_groups(subs.program_id)

        text = "Упс. Кажется, я не смог найти такую группу. Попробуй ещё раз."
        buttons = list(map(lambda group: group.name, groups))
        return Response(text, buttons)


def process_events(current_date: date, callback):
    from_date, to_date = get_week_boundaries(current_date)
    subs = subs_service.get_all()
    subs = list(filter(lambda sub: sub.state == STATE.SAVED_GROUP, subs))
    for sub in subs:
        days = spbu_service.get_events(sub.group_id, from_date, to_date)
        events = next((day for day in days if day.day_date == current_date), None)
        callback(sub.chat_id, events)


def check_state(chat_id, state):
    try:
        return subs_service.get_by_chat_id(chat_id).state == state
    except NotFoundException:
        return None
