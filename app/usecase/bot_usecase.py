import app.service.subs.subs_service as subs_service
import app.service.timetable.timetable_service as spbu_service
from app.domain.subs_types import *
from app.domain.timetable_types import *


def start(chat_id) -> List[Division]:
    subs_service.create_subs(Subscription(chat_id=chat_id, state=STATE.START))
    return spbu_service.get_divisions()


def enter_division(chat_id, division_name) -> List[StudyLevel]:
    division = spbu_service.get_division(division_name)
    subs = subs_service.get_by_chat_id(chat_id)
    subs.division_alias = division.alias
    subs.state = STATE.SAVED_DIVISION
    subs_service.update(subs)
    return spbu_service.get_levels(division.alias)


def retry_enter_division(chat_id) -> List[Division]:
    subs_service.create_subs(Subscription(chat_id=chat_id, state=STATE.START))
    return spbu_service.get_divisions()


def enter_level(chat_id, level_name) -> List[StudyProgram]:
    subs = subs_service.get_by_chat_id(chat_id)
    level = spbu_service.get_level(subs.division_alias, level_name)
    subs.level = level.name
    subs.state = STATE.SAVED_LEVEL
    subs_service.update(subs)
    return level.programs


def retry_enter_level(chat_id) -> List[StudyLevel]:
    subs = subs_service.get_by_chat_id(chat_id)
    return spbu_service.get_levels(subs.division_alias)


def enter_program(chat_id, program_name) -> List[Admission]:
    subs = subs_service.get_by_chat_id(chat_id)
    program = spbu_service.get_program(subs.division_alias, subs.level, program_name)
    subs.program = program.name
    subs.state = STATE.SAVED_PROGRAM
    subs_service.update(subs)
    return program.admissions


def retry_enter_program(chat_id) -> List[StudyProgram]:
    subs = subs_service.get_by_chat_id(chat_id)
    level = spbu_service.get_level(subs.division_alias, subs.level)
    return level.programs


def enter_year(chat_id, year) -> List[Group]:
    subs = subs_service.get_by_chat_id(chat_id)
    admission = spbu_service.get_admission(subs.division_alias, subs.level, subs.program, year)
    subs.year = admission.year
    subs.program_id = admission.program_id
    subs.state = STATE.SAVED_PROGRAM_ID
    subs_service.update(subs)
    return spbu_service.get_groups(admission.program_id)


def retry_enter_year(chat_id) -> List[Admission]:
    subs = subs_service.get_by_chat_id(chat_id)
    program = spbu_service.get_program(subs.division_alias, subs.level, subs.program)
    return program.admissions


def entering_group(chat_id, group_name):
    subs = subs_service.get_by_chat_id(chat_id)
    group = spbu_service.get_group(subs.program_id, group_name)
    subs.group_id = group.id
    subs.state = STATE.SAVED_GROUP
    subs_service.update(subs)


def retry_enter_group(chat_id) -> List[Group]:
    subs = subs_service.get_by_chat_id(chat_id)
    return spbu_service.get_groups(subs.program_id)


def check_state(chat_id, state):
    return subs_service.get_state(chat_id) == state
