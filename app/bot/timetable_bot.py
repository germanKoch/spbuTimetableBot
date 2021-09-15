import telebot
import telebot.types as types

import app.config as config
import app.usecase.bot_usecase as usecase
from app.domain.subs_types import *
from app.domain.timetable_types import *

bot = telebot.TeleBot(config.TOKEN)


def start():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start", "retry"])
def cmd_start(message):
    response = usecase.start(message.chat.id)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(2, response.buttons))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.START))
def entering_division(message):
    bot.send_message(message.chat.id, "Ищу твой факультет. Требуется немного подождать...")
    response = usecase.enter_division(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_DIVISION))
def entering_level(message):
    response = usecase.enter_level(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_LEVEL))
def entering_program(message):
    response = usecase.enter_program(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM))
def entering_year(message):
    response = usecase.enter_year(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


@bot.message_handler(func=lambda message: usecase.check_state(message.chat.id, STATE.SAVED_PROGRAM_ID))
def entering_group(message):
    response = usecase.entering_group(message.chat.id, message.text)
    bot.send_message(message.chat.id, response.text, reply_markup=get_buttons(1, response.buttons))


def send_day_events():
    today = date(2021, 5, 12)
    usecase.process_events(today, lambda chat_id, events: bot.send_message(chat_id, map_day(events)))


def get_buttons(row_width, items):
    markup = types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=True)
    buttons = list(map(lambda item: types.KeyboardButton(text=item), items))
    markup.add(*buttons)
    return markup


def map_day(day: Day) -> str:
    representation = str()
    representation += '\n\n' + day.day_string + '\n\n'
    for event in day.events:
        representation += "Предмет: " + event.subject + "\n"
        representation += "Преподаватели: " + event.educators + "\n"
        representation += "Начало: " + event.start_datetime.time().isoformat()
        representation += ", Конец: " + event.end_datetime.time().isoformat()
        representation += "\n\n"
    return representation
