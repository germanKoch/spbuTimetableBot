import logging
from datetime import timedelta
from typing import List

import telebot
import telebot.types as types

import app.config as config
import app.usecase.get_events_usecase as event_usecase
import app.usecase.register_usecase as register_usecase
import app.util.time_util as time_util
from app.domain.subs_types import *

bot = telebot.TeleBot(config.TOKEN)
log = logging.getLogger(__name__)


def start():
    bot.set_my_commands(_get_commands())
    bot.polling(none_stop=True)


# Команды регистарции пользователя
@bot.message_handler(commands=["start", "retry"])
def cmd_start(message):
    bot.send_message(message.chat.id,
                     f"Привет! Я бот расписаний СПбГУ. Давай немного расскажу про себя. \n"
                     f"Я буду присылать тебе расписание каждый день в {config.SCHEDULER_TIME}.\n"
                     f"Доступные команды: {_get_commands_as_str()}")
    log.debug('cmd_start(chat_id=%s)', message.chat.id)
    response = register_usecase.start(message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=_get_buttons(2, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.START))
def entering_division(message):
    log.debug('entering_division(chat_id=%s, division=%s)', message.chat.id, message.text)
    bot.send_message(message.chat.id, "Ищу твой факультет. Требуется немного подождать...")
    response = register_usecase.enter_division(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=_get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_DIVISION))
def entering_level(message):
    log.debug('entering_level(chat_id=%s, level=%s)', message.chat.id, message.text)
    response = register_usecase.enter_level(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=_get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_LEVEL))
def entering_program(message):
    log.debug('entering_program(chat_id=%s, program=%s)', message.chat.id, message.text)
    response = register_usecase.enter_program(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=_get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM))
def entering_year(message):
    log.debug('entering_year(chat_id=%s, year=%s)', message.chat.id, message.text)
    response = register_usecase.enter_year(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=_get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM_ID))
def entering_group(message):
    log.debug('entering_group(chat_id=%s, group=%s)', message.chat.id, message.text)
    response = register_usecase.entering_group(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    log.debug('unsubscribe(chat_id=%s)', message.chat.id)
    response = register_usecase.unsubscribe(message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    log.debug('subscribe(chat_id=%s)', message.chat.id)
    response = register_usecase.subscribe(message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=types.ReplyKeyboardRemove())


# Команды получения данных
@bot.message_handler(commands=["day"])
def get_day_events(message):
    log.debug('get_day_events(chat_id=%s)', message.chat.id)
    response = event_usecase.get_day_events(time_util.get_current_date(), message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=["tom"])
def get_tomorrow_events(message):
    log.debug('get_tomorrow_events(chat_id=%s)', message.chat.id)
    day = time_util.get_current_date() + timedelta(days=1)
    response = event_usecase.get_day_events(day, message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=["commands"])
def get_commands(message):
    log.debug('get_commands(chat_id=%s)', message.chat.id)
    bot.send_message(message.chat.id, f"Доступные команды: {_get_commands_as_str()}",
                     reply_markup=types.ReplyKeyboardRemove())


def send_day_events():
    log.debug('send_day_events()')
    event_usecase.get_day_events_all(
        lambda chat_id, text: bot.send_message(chat_id, text, reply_markup=types.ReplyKeyboardRemove()))


def _get_buttons(row_width, items):
    markup = types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=True)
    buttons = list(map(lambda item: types.KeyboardButton(text=item), items))
    markup.add(*buttons)
    return markup


def _get_commands_as_str() -> str:
    return ''.join(map(lambda command: '\n/' + command.command + ' - ' + command.description, _get_commands()))


def _get_commands() -> List[types.BotCommand]:
    return [
        types.BotCommand(command="day", description="получить расписание на день"),
        types.BotCommand(command="tom", description="получить расписание на завтра"),
        types.BotCommand(command="retry", description="пройти регистрацию заново, если что-то не так"),
        types.BotCommand(command="unsubscribe", description="отписаться от рассылки"),
        types.BotCommand(command="subscribe", description="подписаться повторно"),
        types.BotCommand(command="commands", description="узнать доступные команды")
    ]
