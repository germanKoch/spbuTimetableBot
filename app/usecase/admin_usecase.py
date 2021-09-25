from app.domain.exception.invalid_credentials_exception import InvalidCredentialsException
from app.domain.gen_response import GenResponse
from app.domain.response import Response
import app.config as config


def send_message(password, admin_chat_id, chat_id, message) -> GenResponse:
    try:
        _check_pass(password)
    except InvalidCredentialsException:
        return GenResponse(admin_chat_id, 'Неверный пароль', [])
    return GenResponse(chat_id, message)


def _check_pass(password):
    if password != config.ADMIN_PASS:
        raise InvalidCredentialsException
