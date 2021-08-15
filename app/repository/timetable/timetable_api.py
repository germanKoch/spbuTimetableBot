import spbu
from spbu.types import *
from app.repository.timetable.timetable_types import *


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
    return Day(day_string=day.day_string, events=events)


class TimetableApi:

    def __init__(self):
        self.divisions_cache = []
        self.levels_cache = dict()

    def get_divisions(self) -> List[Division]:
        if len(self.divisions_cache) == 0:
            divisions = spbu.studydivisions.get_study_divisions()
            self.divisions_cache = list(map(map_division, divisions))
        return self.divisions_cache

    def get_levels_by_alias(self, alias: str) -> List[StudyLevel]:
        if alias not in self.levels_cache:
            levels = spbu.studydivisions.get_study_levels(alias)
            self.levels_cache[alias] = list(map(map_level, levels))
        return self.levels_cache[alias]

    def get_groups_by_program_id(self, program_id: int) -> List[Group]:
        groups = spbu.programs.get_groups(program_id)
        return list(map(map_group, groups))

    def get_events(self, group_id: int, from_date: date, to_date: date):
        response = spbu.groups.get_group_events(group_id=group_id, from_date=from_date, to_date=to_date)
        return list(map(map_day, response.days))


api = TimetableApi()
