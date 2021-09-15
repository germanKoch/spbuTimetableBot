from typing import List


class Response:
    text: str
    buttons: List[str]

    def __init__(self, text, buttons):
        self.text = text
        self.buttons = buttons
