from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from BattleshipGame.rules import beautiful_coordinates_input, create_new_game
from dbcommands import db_data_input, db_data_output
from imagerender import create_picture
from configparser import ConfigParser
from requests import post
from pathlib import Path
import logging


def start(bot, update):
    user_id = update.message.chat.id
    user_username = update.message.chat.username
    print(f"> new user connected (ID: {user_id}, NAME: {user_username})")

    keyboard_markup = ReplyKeyboardMarkup([['/startnewgame', '/info', '/statistic']])

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


def startnewgame(bot, update):
    player1.data_erase(), player2.data_erase()
    ai.memory = None

    player1.ships.auto_ships_deploy()
    player2.ships.auto_ships_deploy()

    db_data_input(update, player1.data_output(), player2.data_output())

    keyboard_markup = ReplyKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=update.message.chat_id,
        text='starting game...\nYour field:',
        reply_markup=keyboard_markup
    )
    image_sender(update.message.chat_id, player1.field)


def shoot(bot, update):
    chat_id = update.message.chat_id
    if update.message.text in [k for i in keyboard for k in i]:
        coordinates = beautiful_coordinates_input(False, update.message.text)

        db_data = db_data_output(update)
        if not db_data:
            bot.send_message(
                chat_id=chat_id,
                text="You don't have any game\n\nWrite /startnewgame"
            )
            return

        field_data, enemy_data, memory = db_data
        player1.data_input(field_data)
        player2.data_input(enemy_data)
        ai.memory_input(memory)

        result = player1.control.shoot(player2, *coordinates)
        message = str(result)

        if result != 'Error':
            enemy_result = ai.auto_shoot(player1)
            image_sender(chat_id, player1.enemy_field)

            if enemy_result in ('hit', 'kill'):
                bot.send_message(chat_id=chat_id, text='Enemy hit your ship!')
                image_sender(chat_id, player1.field)
            else:
                bot.send_message(chat_id=chat_id, text='Enemy missed!')

            player_data = player1.data_output()
            enemy_data = player2.data_output()
            ai_memory = ai.memory_output()
            db_data_input(update, player_data, enemy_data, ai_memory)

        else:
            message = 'You already shoot in this coordinates!'

    else:
        message = 'Wrong coordinates!'

    bot.send_message(chat_id=update.message.chat_id, text=message)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Unknown command :(')


def image_sender(chat_id, player_field):
    files = {'photo': create_picture(player_field)}
    status = post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}",
        files=files
    )
    return status


if __name__ == "__main__":
    print('> starting bot...')

    # config settings
    config = ConfigParser()
    if not Path('__file__').resolve().parent.joinpath('config.ini').exists():
        config['Bot'] = {'Token': 'None'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    config.read('config.ini')
    TOKEN = config['Bot']['Token']

    # log settings
    logging.basicConfig(filename='botlog.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

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

    weather_handler = CommandHandler('startnewgame', startnewgame)  # Обработка команды /startnewgame
    dispatcher.add_handler(weather_handler)

    shoot_handler = MessageHandler(Filters.regex(r'^[A-Ja-j](\d|10)$'), shoot)  # Обработка выстрела
    dispatcher.add_handler(shoot_handler)

    unknown_command = MessageHandler(Filters.text, unknown)
    dispatcher.add_handler(unknown_command)

    # bot's start
    updater.start_polling()
    # bot's end
    updater.idle()
