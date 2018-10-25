__author__ = 'alexsviridov'

# import telebot

BOT_TOKEN = "660361487:AAFBBtv8y1pfqY-pPekyT3Qbom9RMWD0Glg"

# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

#BOT_TOKEN = "TOKEN"
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(BOT_TOKEN)


dispatcher = updater.dispatcher

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CalcBot:
    Value = 0
    def __init__(self):
        self.Value = 0

    def parseValue(self, text):
        try:
            return float(text)
        except ValueError:
            return 0.0

    def calulate(self, text):
        v = self.parseValue(text)
        self.Value += v



calc = CalcBot()


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def textMessage(bot, update):
    calc.calulate(update.message.text)
    response = '>> ' + update.message.text + ' = ' + calc.Value
#    response = '>> ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
#updater.start_polling(clean=True)

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=BOT_TOKEN)
updater.bot.set_webhook("https://peaceful-hamlet-47591.herokuapp.com/" + BOT_TOKEN)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()