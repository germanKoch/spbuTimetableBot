import app.service.subs.subs_service as subs_service
import app.service.timetable.timetable_service as spbu_service

from app.domain.timetable_types import *


def start(chat_id) -> List[Division]:
    subs_service.create_subs(chat_id)
    return spbu_service.get_divisions()


def enter_division(chat_id, division_name) -> List[StudyLevel]:
    division = spbu_service.get_division(division_name)
    subs_service.set_division(chat_id, division.alias)
    return spbu_service.get_levels(division.alias)


def enter_level(chat_id, level_name) -> List[StudyProgram]:
    subs = subs_service.get_by_chat_id(chat_id)
    level = spbu_service.get_level(subs.division_alias, level_name)
    subs_service.set_level(chat_id, level.name)
    return level.programs


def enter_program(chat_id, program_name) -> List[Admission]:
    subs = subs_service.get_by_chat_id(chat_id)
    program = spbu_service.get_program(subs.division_alias, subs.level, program_name)
    subs_service.set_program(chat_id, program.name)
    return program.admissions


def enter_year(chat_id, year) -> List[Group]:
    subs = subs_service.get_by_chat_id(chat_id)
    admission = spbu_service.get_admission(subs.division_alias, subs.level, subs.program, year)
    # TODO: смену статсуов вынеснти сюда
    # TODO: сделать аналог ORM. СОхранять всю сущность
    subs_service.set_year(chat_id, admission.year)
    subs_service.set_program_id(chat_id, admission.program_id)

    return spbu_service.get_groups(admission.program_id)


def entering_group(chat_id, group_name):
    subs = subs_service.get_by_chat_id(chat_id)
    group = spbu_service.get_group(subs.program_id, group_name)
    subs_service.set_group_id(chat_id, group.id)


def check_state(chat_id, state):
    return subs_service.get_state(chat_id) == state
