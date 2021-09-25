from typing import List

from app.domain.response import Response


class GenResponse(Response):
    chat_id: str

    def __init__(self, chat_id, text, buttons):
        Response.__init__(self=self, text=text, buttons=buttons)
        self.chat_id = chat_id
