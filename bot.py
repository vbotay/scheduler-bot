import telebot

import config
from utils import tools
from utils.scheduler import Scheduler
from utils.decorators import check_new_day

bot = telebot.TeleBot(config.TOKEN)

scheduler = Scheduler()
from utils.tools import TimeFormatError
from utils.tools import DeletionError
from utils.tools import MembersError
from utils.tools import TimingError


@bot.message_handler(commands=['schedule'])
@check_new_day
def show_schedule(message):
    schedule = scheduler.print_schedule()
    # TODO format output
    bot.send_message(message.chat.id, str(schedule))


@bot.message_handler(commands=['add'])
@check_new_day
def add_to_game(message):
    game_time = tools.get_command_params(message)
    user = tools.get_username(message)
    try:
        msg = scheduler.add_to_schedule(game_time, user)
        bot.send_message(message.chat.id, msg)
    except (TimeFormatError, MembersError, TimingError) as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands=['del'])
@check_new_day
def delete_from_game(message):
    game_time = tools.get_command_params(message)
    user = tools.get_username(message)

    try:
        msg = scheduler.delete_from(game_time, user)
        bot.send_message(message.chat.id, msg)
    except DeletionError as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands=['me', 'myschedule'])
@check_new_day
def show_my_schedule(message):
    user = tools.get_username(message)
    schedule = scheduler.my_games(user)
    bot.send_message(message.chat.id, schedule)


@bot.message_handler(commands=['team'])
@check_new_day
def show_team(message):
    prm = tools.get_command_params(message)
    try:
        msg = scheduler.print_team(prm)
        bot.send_message(message.chat.id, msg)
    except MembersError as e:
        bot.send_message(message.chat.id, e)

