import spbu
import logging
from spbu.types import *
from app.domain.timetable_types import *

log = logging.getLogger(__name__)


def get_divisions() -> List[Division]:
    divisions = spbu.studydivisions.get_study_divisions()
    log.debug('get_divisions -> %s', divisions)
    return list(map(map_division, divisions))


def get_levels_by_alias(alias: str) -> List[StudyLevel]:
    levels = spbu.studydivisions.get_study_levels(alias)
    log.debug('get_levels_by_alias -> %s', levels)
    return list(map(map_level, levels))


def get_groups_by_program_id(program_id: int) -> List[Group]:
    groups = spbu.programs.get_groups(program_id)
    log.debug('get_groups_by_program_id -> %s', groups)
    return list(map(map_group, groups))


def get_events(group_id: int, from_date: date, to_date: date) -> List[Day]:
    response = spbu.groups.get_group_events(group_id=group_id, from_date=from_date, to_date=to_date)
    days = response.days
    log.debug('get_events -> %s', days)
    return list(map(map_day, days))


def map_division(div: SDStudyDivision):
    return Division(name=div.name, alias=div.alias)


def map_admission(adm: SDPLAdmissionYear):
    return Admission(program_id=adm.study_program_id, year=adm.year_name)


def map_group(group: PGGroup):
    return Group(id=group.student_group_id, name=group.student_group_name)


def map_program(prog: SDPLProgramCombination):
    admissions = list(map(map_admission, prog.admission_years))
    return StudyProgram(name=prog.name, admissions=admissions)


def map_level(lev: SDPLStudyLevel):
    programs = list(map(map_program, lev.study_program_combinations))
    return StudyLevel(name=lev.study_level_name, programs=programs)


def map_event(event: GEEvent):
    return Event(start_datetime=event.start, end_datetime=event.end, subject=event.subject,
                 educators=event.educators_display_text, locations=event.locations_display_text)


def map_day(day: GEEventsDay):
    events = list(map(map_event, day.day_study_events))
    return Day(day_date=day.day, day_string=day.day_string, events=events)
