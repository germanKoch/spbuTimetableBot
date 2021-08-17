from typing import Dict

import app.repository.timetable.timetable_api as api

from app.domain.exception.not_found_exception import NotFoundException
from app.domain.timetable_types import *


class Cache:
    divisions: List[Division] = []
    levels: Dict[str, List[StudyLevel]] = dict()

    def is_empty_divisions(self):
        return len(self.divisions) == 0

    def is_empty_levels(self, alias):
        return alias not in self.levels


cache = Cache()


def warm_divisions():
    if cache.is_empty_divisions():
        cache.divisions = api.get_divisions()


def warm_levels(alias: str):
    if cache.is_empty_levels(alias):
        cache.levels[alias] = api.get_levels_by_alias(alias)


def get_divisions() -> List[Division]:
    warm_divisions()
    return cache.divisions


def get_division(name: str) -> Division:
    warm_divisions()
    for div in cache.divisions:
        if div.name == name:
            return div
    raise NotFoundException("division not found")


def get_levels(alias: str) -> List[StudyLevel]:
    warm_levels(alias)
    return cache.levels[alias]


def get_level(alias: str, name: str) -> StudyLevel:
    warm_levels(alias)
    for level in cache.levels[alias]:
        if level.name == name:
            return level
    raise NotFoundException("level not found")


def get_program(alias: str, level_name: str, program_name: str) -> StudyProgram:
    level = get_level(alias, level_name)
    for program in level.programs:
        if program.name == program_name:
            return program
    raise NotFoundException("program not found")


def get_admission(alias: str, level_name: str, program_name: str, year: str) -> Admission:
    program = get_program(alias, level_name, program_name)
    for admission in program.admissions:
        if admission.year == year:
            return admission
    raise NotFoundException("admission not found")


def get_groups(program_id: int):
    groups = api.get_groups_by_program_id(program_id)
    if len(groups) == 0:
        raise NotFoundException("groups not found")
    return groups


def get_group(program_id: int, name: str):
    groups = get_groups(program_id)
    for group in groups:
        if group.name == name:
            return group
    raise NotFoundException("group not found")
