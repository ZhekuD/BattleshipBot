# BattleshipBot
Battleship game bot for Telegram written in Python using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Description
BattleshipBot consists of two parts:
* **BattleshipGame module.** This contains logic for the game. It has text interface so you can install and/or launch it separately via console. Just write *"python3 -m BattleshipGame"* when you are in the bot's root.
* **Telegram Bot.** It transmits game logic to Telegram. Read *Usage*.


## Usage
When you launch *bot.py* for the first time, it will automatically create a SQLite database, config.ini file and log file. In the config file you need to write your bot's [token](https://core.telegram.org/bots/api#authorizing-your-bot). After that reboot the bot. You can create database manually. Just use *create_table* function from *dbcommands.py* file.

