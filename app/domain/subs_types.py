class STATE:
    START = "0"
    SAVED_DIVISION = "1"
    SAVED_LEVEL = "2"
    SAVED_PROGRAM = "3"
    SAVED_YEAR = "4"
    SAVED_PROGRAM_ID = "5"
    SAVED_GROUP = "6"


class Subscription:
    chat_id: int
    state: str
    division_alias: str
    level: str
    program: str
    year: str
    program_id: str
    group_id: int

    def __init__(self, chat_id: int = None, state: str = None, division_alias: str = None,
                 level: str = None, program: str = None, year: str = None, program_id: str = None, group_id: int = 0):
        self.chat_id = chat_id
        self.state = state
        self.division_alias = division_alias
        self.level = level
        self.program = program
        self.year = year
        self.program_id = program_id
        self.group_id = group_id

    def __repr__(self):
        return f"Subscription({self.chat_id}, {self.state}, {self.division_alias},{self.level}, {self.program} ,{self.year}, {self.group_id} )"
