class STATE():
    START = "0"
    ENTER_DIVISION = "1"
    ENTER_LEVEL = "2"
    ENTER_PROGRAM = "3"
    ENTER_YEAR = "4"
    ENTER_GROUP = "5"
    COMPLETE = "6"


class Subscription():
    chat_id: str
    state: str = ""
    division_alias: str = ""
    level: str = ""
    program: str = ""
    year: str = ""
    program_id: str = ""
    group_id: int = 0

    def __repr__(self):
        return f"Subscription({self.chat_id}, {self.state}, {self.division_alias},{self.level}, {self.program} ,{self.year}, {self.group_id} )"
