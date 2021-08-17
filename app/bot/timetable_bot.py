from datetime import date

import telebot
import telebot.types as types

import app.config as config
import app.service.subs.subs_service as subs_service
import app.service.timetable.timetable_service as spbu_service
from app.domain.subs_types import *
from app.util.week_util import get_week_boundaries

bot = telebot.TeleBot(config.TOKEN)


def start():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    subs_service.create_subs(message.chat.id)
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    divisions = spbu_service.get_divisions()

    buttons = list(map(lambda div: types.KeyboardButton(text=div.name), divisions))
    markup.add(*buttons)

    bot.send_message(message.chat.id, f"Привет! Я бот расписаний. Выбери факультет", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.START)
def entering_division(message):
    division = spbu_service.get_division(message.text)
    subs_service.set_division(message.chat.id, division.alias)

    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    levels = spbu_service.get_levels(division.alias)

    buttons = list(map(lambda lev: types.KeyboardButton(text=lev.name), levels))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Уровень", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.SAVED_DIVISION)
def entering_level(message):
    subs_service.set_level(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    subs = subs_service.get_by_chat_id(message.chat.id)
    level = spbu_service.get_level(subs.division_alias, subs.level)

    buttons = list(map(lambda prog: types.KeyboardButton(text=prog.name), level.programs))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Программа", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.SAVED_LEVEL)
def entering_program(message):
    subs_service.set_program(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    subs = subs_service.get_by_chat_id(message.chat.id)
    program = spbu_service.get_program(subs.division_alias, subs.level, subs.program)

    buttons = list(map(lambda adm: types.KeyboardButton(text=adm.year), program.admissions))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Год", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.SAVED_PROGRAM)
def entering_year(message):
    subs = subs_service.get_by_chat_id(message.chat.id)
    admission = spbu_service.get_admission(subs.division_alias, subs.level, subs.program, message.text)
    subs_service.set_year(message.chat.id, admission.year)
    subs_service.set_program_id(message.chat.id, admission.program_id)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    groups = spbu_service.get_groups(admission.program_id)
    buttons = list(map(lambda gr: types.KeyboardButton(text=gr.name), groups))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Группа", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.SAVED_PROGRAM_ID)
def entering_group(message):
    subs = subs_service.get_by_chat_id(message.chat.id)
    group = spbu_service.get_group(subs.program_id, message.text)

    subs_service.set_group_id(message.chat.id, group.id)
    bot.send_message(message.chat.id, "Отлично! Зареган")


@bot.message_handler(commands=["week"])
def get_week_events(message):
    today = date(2021, 5, 11)
    start_week, end_week = get_week_boundaries(today)
    print(start_week, end_week)
    print(api.get_events(275938, from_date=start_week, to_date=end_week))
    return None
