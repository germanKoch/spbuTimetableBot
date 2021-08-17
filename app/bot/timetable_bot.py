from datetime import date

import telebot
import telebot.types as types

import app.config as config
import app.usecase.bot_usecase as usecase
from app.domain.subs_types import *
from app.util.week_util import get_week_boundaries

bot = telebot.TeleBot(config.TOKEN)


def start():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    divisions = usecase.start(message.chat.id)

    bot.send_message(message.chat.id, f"Привет! Я бот расписаний. Выбери факультет",
                     reply_markup=get_buttons(2, divisions, lambda div: div.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.START))
def entering_division(message):
    levels = usecase.enter_division(message.chat.id, message.text)

    bot.send_message(message.chat.id, "Отлично! Уровень", reply_markup=get_buttons(1, levels, lambda lev: lev.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_DIVISION))
def entering_level(message):
    programs = usecase.enter_level(message.chat.id, message.text)

    bot.send_message(message.chat.id, "Отлично! Программа", reply_markup=get_buttons(1, programs, lambda pr: pr.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_LEVEL))
def entering_program(message):
    admissions = usecase.enter_program(message.chat.id, message.text)

    bot.send_message(message.chat.id, "Отлично! Год", reply_markup=get_buttons(1, admissions, lambda ad: ad.year))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM))
def entering_year(message):
    groups = usecase.enter_year(message.chat.id, message.text)

    bot.send_message(message.chat.id, "Отлично! Группа", reply_markup=get_buttons(1, groups, lambda gr: gr.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM_ID))
def entering_group(message):
    usecase.entering_group(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Отлично! Зареган")


def get_buttons(row_width, items, mapper):
    markup = types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=True)
    buttons = list(map(lambda item: types.KeyboardButton(text=mapper(item)), items))
    markup.add(*buttons)
    return markup

# @bot.message_handler(commands=["week"])
# def get_week_events(message):
#     today = date(2021, 5, 11)
#     start_week, end_week = get_week_boundaries(today)
#     print(start_week, end_week)
#     print(api.get_events(275938, from_date=start_week, to_date=end_week))
#     return None
