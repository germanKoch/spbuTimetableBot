import logging

import telebot
import telebot.types as types
import datetime as dt
import app.config as config
import app.usecase.get_events_usecase as event_usecase
import app.usecase.register_usecase as register_usecase
from app.domain.subs_types import *
import time

bot = telebot.TeleBot(config.TOKEN)
log = logging.getLogger(__name__)


def start():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start", "retry"])
def cmd_start(message):
    bot.send_message(message.chat.id,
                     f"Привет! Я бот расписаний СПбГУ. Давай немного расскажу про себя. \n"
                     f"Я буду присылать тебе расписание каждый день в {config.SCHEDULER_TIME}.\n"
                     f"Доступные команды: \n"
                     f"/day - получить расписание на день.\n"
                     f"/retry - пройти регистрацию заново, если что-то пойдёт не так.\n")
    log.debug('cmd_start(chat_id=%s)', message.chat.id)
    response = register_usecase.start(message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(2, response.buttons))


@bot.message_handler(commands=["day"])
def get_day_events(message):
    log.debug('get_day_events(chat_id=%s)', message.chat.id)
    response = event_usecase.get_day_events(message.chat.id)
    bot.send_message(message.chat.id, response.text)


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.START))
def entering_division(message):
    log.debug('entering_division(chat_id=%s, division=%s)', message.chat.id, message.text)
    bot.send_message(message.chat.id, "Ищу твой факультет. Требуется немного подождать...")
    response = register_usecase.enter_division(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_DIVISION))
def entering_level(message):
    log.debug('entering_level(chat_id=%s, level=%s)', message.chat.id, message.text)
    response = register_usecase.enter_level(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_LEVEL))
def entering_program(message):
    log.debug('entering_program(chat_id=%s, program=%s)', message.chat.id, message.text)
    response = register_usecase.enter_program(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM))
def entering_year(message):
    log.debug('entering_year(chat_id=%s, year=%s)', message.chat.id, message.text)
    response = register_usecase.enter_year(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: register_usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM_ID))
def entering_group(message):
    log.debug('entering_group(chat_id=%s, group=%s)', message.chat.id, message.text)
    response = register_usecase.entering_group(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


def send_day_events():
    log.debug('send_day_events()')
    event_usecase.get_day_events_all(bot.send_message)


def get_buttons(row_width, items):
    markup = types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=True)
    buttons = list(map(lambda item: types.KeyboardButton(text=item), items))
    markup.add(*buttons)
    return markup
