from datetime import datetime
from datetime import date
from typing import List


class Division:
    name: str
    alias: str

    def __init__(self, name, alias):
        self.alias = alias
        self.name = name

    def __repr__(self):
        return f"Division({self.name}, {self.alias})"


class Admission:
    program_id: int
    year: str

    def __init__(self, program_id, year):
        self.program_id = program_id
        self.year = year

    def __repr__(self):
        return f"Admission({self.program_id}, {self.year})"


class StudyProgram:
    name: str
    admissions: List[Admission]

    def __init__(self, name, admissions):
        self.name = name
        self.admissions = admissions

    def __repr__(self):
        return f"StudyProgram({self.name}, {self.admissions})"


class StudyLevel:
    name: str
    programs: List[StudyProgram]

    def __init__(self, name, programs):
        self.name = name
        self.programs = programs

    def __repr__(self):
        return f"StudyLevel({self.name}, {self.programs})"


class Group:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Group({self.id}, {self.name})"


class Event:
    start_datetime: datetime
    end_datetime: datetime
    subject: str
    educators: str
    locations: List[str]

    def __init__(self, start_datetime, end_datetime, subject, educators, locations):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.subject = subject
        self.educators = educators
        self.locations = locations

    def __repr__(self):
        return f"Event({self.start_datetime}, {self.end_datetime}, {self.subject}, {self.educators}, {self.locations})"


class Day:
    day_date: date
    day_string: str
    events: List[Event]

    def __init__(self, day_date, day_string, events):
        self.day_date = day_date
        self.day_string = day_string
        self.events = events

    def __repr__(self):
        return f"Day({self.day_date}, {self.day_string}, {self.events})"
