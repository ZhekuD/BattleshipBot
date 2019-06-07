from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from BattleshipGame.rules import Player, beautiful_coordinates_input, create_new_game
from BattleshipGame.ai import AI
from imagerender import create_picture
from configparser import ConfigParser
import sqlite3
import logging


def start(bot, update):
    user_id = update.message.chat.id
    user_username = update.message.chat.username
    print(f"> new user connected (ID: {user_id}, NAME: {user_username})")

    keyboard_markup = ReplyKeyboardMarkup([['/startnewgame', '/info']])

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"I'm a bot and you are my Master, please talk to me, {update.message.chat.first_name}!",
        reply_markup=keyboard_markup
    )


def info(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I'm a bot, that can play battleship with you!"
    )


def startnewgame(bot, update, args):

    player1.ships.auto_ships_deploy()
    player2.ships.auto_ships_deploy()

    pic = create_picture(player1.field)
    print(pic)

    keyboard_markup = ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text=r'starting game...', reply_markup=keyboard_markup)


def shoot(bot, update):
    if update.message.text in [k for i in keyboard for k in i]:
        coordinates = beautiful_coordinates_input(False, update.message.text)
        result = player1.control.shoot(player2, *coordinates)
        ai.auto_shoot(player1)
        message = str(result) if result != 'Error' else 'You already shoot in this coordinates!'
    else:
        message = 'Wrong coordinates!'

    bot.send_message(chat_id=update.message.chat_id, text=message)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Unknown command :(')


if __name__ == "__main__":
    print('> starting bot...')

    # config settings
    config = ConfigParser()
    config.read('config.ini')
    TOKEN = config['Bot']['BotToken']

    # log settings
    logging.basicConfig(filename='botlog.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # connect to db
    sqlite3.connect('./database.sql')

    # create Player's objects
    player1, player2, ai = create_new_game(ai=True)

    # create pattern for keyboard
    alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
    keyboard = [[alpha + str(num) for alpha in alphabet] for num in range(1, 11)]

    # bot settings
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)  # Обработка команды /start
    dispatcher.add_handler(start_handler)

    info_handler = CommandHandler('info', info)  # Обработка команды /info
    dispatcher.add_handler(info_handler)

    weather_handler = CommandHandler('startnewgame', startnewgame, pass_args=True)  # Обработка команды /startnewgame
    dispatcher.add_handler(weather_handler)

    shoot_handler = MessageHandler(Filters.regex(r'^[A-Ja-j](\d|10)$'), shoot)  # Обработка выстрела
    dispatcher.add_handler(shoot_handler)

    unknown_command = MessageHandler(Filters.text, unknown)
    dispatcher.add_handler(unknown_command)

    # bot's start
    updater.start_polling()


