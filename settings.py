import os

HELP_MESSAGE = os.getenv('HELP_MESSAGE', 'Введите число и код валюты.\nНапример:\n15000 eur')
DEFAULT_ANSWER = os.getenv('TG_BOT_TOKEN', 'Команда не распознана.\n' + HELP_MESSAGE)

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
if TG_BOT_TOKEN is None:
    raise AttributeError("Введите токен телеграмм бота как TG_BOT_TOKEN в environment")

CURRENCY_API_TOKEN = os.getenv('CURRENCY_API_TOKEN')
if CURRENCY_API_TOKEN is None:
    raise AttributeError("Введите токен апи конвертации валют как CURRENCY_API_TOKEN в environment")
