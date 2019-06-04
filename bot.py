from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from BattleshipGame.rules import Player, beautiful_coordinates_input
from BattleshipGame.interface import Interface
from BattleshipGame.ai import AI
import logging


def start(bot, update):
    user_id = update.message.chat.id
    user_username = update.message.chat.username
    print(f"> new user connected (ID: {user_id}, NAME: {user_username})")
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"""I'm a bot and you are my Master, please talk to me, {update.message.chat.first_name}!

You can control me by sending these commands:
/info - show info about me 
/weather - show weather in your location
"""
    )


def info(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=b"I'm a bot, that can show you weather wherever you want(In the future, perhaps \xF0\x9F\x98\x81)!".decode()
    )


def weather(bot, update, args):
    if args:
        location = args[0]
    else:
        location = None

    bot.send_message(chat_id=update.message.chat_id, text=get_weather(location))


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


if __name__ == "__main__":
    print('> starting bot...')

    logging.basicConfig(filename='botlog.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater = Updater(token='780410802:AAEM_xNdws3JSf3ptR5qiDWGNRypsGvxdJY')

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)  # Обработка команды /start
    dispatcher.add_handler(start_handler)

    info_handler = CommandHandler('info', info)  # Обработка команды /info
    dispatcher.add_handler(info_handler)

    weather_handler = CommandHandler('weather', weather, pass_args=True)  # Обработка команды /weather
    dispatcher.add_handler(weather_handler)

    echo_handler = MessageHandler(Filters.text, echo)  # Обработка обычного сообщения
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
