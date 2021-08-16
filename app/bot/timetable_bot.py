from datetime import date

import telebot
import telebot.types as types

import app.config as config
import app.service.subs_service as subs_service
from app.domain.subs_types import *
from app.repository.timetable.timetable_api import api
from app.util.week_util import get_week_boundaries

bot = telebot.TeleBot(config.TOKEN)


def start():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    subs_service.create_subs(message.chat.id)
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    divisions = api.get_divisions()

    buttons = list(map(lambda div: types.KeyboardButton(text=div.name), divisions))
    markup.add(*buttons)

    bot.send_message(message.chat.id, f"Привет! Я бот расписаний. Выбери факультет", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.START)
def entering_division(message):
    divisions = api.get_divisions()
    alias = next(div for div in divisions if div.name == message.text).alias

    subs_service.set_division(message.chat.id, alias)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    levels = api.get_levels_by_alias(alias)

    buttons = list(map(lambda lev: types.KeyboardButton(text=lev.name), levels))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Уровень", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.ENTER_DIVISION)
def entering_level(message):
    subs_service.set_level(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    subs = subs_service.get_by_id(message.chat.id)
    levels = api.get_levels_by_alias(subs.division_alias)
    programs = next(lev for lev in levels if lev.name == message.text).programs

    buttons = list(map(lambda prog: types.KeyboardButton(text=prog.name), programs))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Программа", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.ENTER_LEVEL)
def entering_program(message):
    subs_service.set_program(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    subs = subs_service.get_by_id(message.chat.id)
    levels = api.get_levels_by_alias(subs.division_alias)
    programs = next(lev for lev in levels if lev.name == subs.level).programs
    admissions = next(prog for prog in programs if prog.name == subs.program).admissions

    buttons = list(map(lambda adm: types.KeyboardButton(text=adm.year), admissions))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Год", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.ENTER_PROGRAM)
def entering_year(message):
    # TODO: сразу ставить program id
    subs = subs_service.get_by_id(message.chat.id)
    levels = api.get_levels_by_alias(subs.division_alias)
    programs = next(lev for lev in levels if lev.name == subs.level).programs
    admissions = next(prog for prog in programs if prog.name == subs.program).admissions
    program_id = next(ad for ad in admissions if ad.year == message.text).program_id

    subs_service.set_year(message.chat.id, message.text)
    subs_service.set_program_id(message.chat.id, program_id)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    # TODO: иногда группы пустые
    groups = api.get_groups_by_program_id(program_id)
    buttons = list(map(lambda gr: types.KeyboardButton(text=gr.name), groups))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Отлично! Группа", reply_markup=markup)


@bot.message_handler(func=lambda message: subs_service.get_state(message.chat.id) == STATE.ENTER_YEAR)
def entering_group(message):
    subs = subs_service.get_by_id(message.chat.id)
    groups = api.get_groups_by_program_id(subs.program_id)
    group_id = next(gr for gr in groups if gr.name == message.text).id

    subs_service.set_group_id(message.chat.id, group_id)
    bot.send_message(message.chat.id, "Отлично! Зареган")


@bot.message_handler(commands=["week"])
def get_week_events(message):
    today = date(2021, 5, 11)
    start_week, end_week = get_week_boundaries(today)
    print(start_week, end_week)
    print(api.get_events(275938, from_date=start_week, to_date=end_week))
    return None
