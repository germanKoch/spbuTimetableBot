import telebot
import telebot.types as types

import app.config as config
import app.usecase.bot_usecase as usecase
from app.domain.subs_types import *
from app.domain.exception.not_found_exception import NotFoundException

bot = telebot.TeleBot(config.TOKEN)


def start():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start", "retry"])
def cmd_start(message):
    divisions = usecase.start(message.chat.id)

    bot.send_message(message.chat.id, f"Привет! Я бот расписаний. Выбери факультет",
                     reply_markup=get_buttons(2, divisions, lambda div: div.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.START))
def entering_division(message):
    try:
        bot.send_message(message.chat.id, "Ищу твой факультет. Требуется немного подождать...")
        levels = usecase.enter_division(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Выбери уровень: ", reply_markup=get_buttons(1, levels, lambda lev: lev.name))
    except NotFoundException:
        divisions = usecase.retry_enter_division(message.chat.id)
        bot.send_message(message.chat.id, "Упс. Кажется, я не смог найти такой факультет. Попробуй ещё раз.",
                         reply_markup=get_buttons(2, divisions, lambda div: div.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_DIVISION))
def entering_level(message):
    try:
        programs = usecase.enter_level(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Отлично! Программа",
                         reply_markup=get_buttons(1, programs, lambda pr: pr.name))
    except NotFoundException:
        levels = usecase.retry_enter_level(message.chat.id)
        bot.send_message(message.chat.id, "Упс. Кажется, я не смог найти такой уровень. Попробуй ещё раз.",
                         reply_markup=get_buttons(1, levels, lambda div: div.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_LEVEL))
def entering_program(message):
    try:
        admissions = usecase.enter_program(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Отлично! Год",
                         reply_markup=get_buttons(1, admissions, lambda ad: ad.year))
    except NotFoundException:
        programs = usecase.retry_enter_program(message.chat.id)
        bot.send_message(message.chat.id, "Упс. Кажется, я не смог найти такую программу. Попробуй ещё раз.",
                         reply_markup=get_buttons(1, programs, lambda div: div.name))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM))
def entering_year(message):
    try:
        groups = usecase.enter_year(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Отлично! Группа",
                         reply_markup=get_buttons(1, groups, lambda gr: gr.name))
    except NotFoundException:
        adms = usecase.retry_enter_year(message.chat.id)
        bot.send_message(message.chat.id, "Упс. Кажется, я не смог найти такой год. Попробуй ещё раз.",
                         reply_markup=get_buttons(1, adms, lambda div: div.year))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM_ID))
def entering_group(message):
    try:
        usecase.entering_group(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Отлично! Зареган")
    except NotFoundException:
        groups = usecase.retry_enter_group(message.chat.id)
        bot.send_message(message.chat.id, "Упс. Кажется, я не смог найти такую группу. Попробуй ещё раз.",
                         reply_markup=get_buttons(1, groups, lambda div: div.name))


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
